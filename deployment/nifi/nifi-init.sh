#!/usr/bin/env bash
set -e

NIFI_URL="${NIFI_URL:-http://nifi:8080}"
NIFI_REGISTRY_URL="${NIFI_REGISTRY_URL:-http://nifiregistry:18080}"
REGISTRY_CLIENT_NAME="nifi-registry"
REGISTRY_CLIENT_URL="http://nifiregistry:18080/nifi-registry"
REGISTRY_BUCKET_NAME="Integrator Framework"

MAX_ATTEMPTS=30
SLEEP_BETWEEN=10

echo "[INFO] Using NiFi URL: $NIFI_URL"

###############################################################################
wait_for_nifi_ready() {
  echo "[INFO] ---------------------------------------"
  echo "[INFO] Waiting for NiFi REST API to become available..."
  for ((ATTEMPT=1; ATTEMPT<=MAX_ATTEMPTS; ATTEMPT++)); do
    HTTP_CODE=$(curl -s -o /tmp/nifi_resp.json -w "%{http_code}" -X GET "$NIFI_URL/nifi-api/flow/registries" || echo "000")
    if [[ "$HTTP_CODE" =~ ^2[0-9]{2}$ ]] && jq . < /tmp/nifi_resp.json >/dev/null 2>&1; then
      echo "[INFO] NiFi REST API is ready."
      break
    fi
    echo "[DEBUG] - NiFi API not ready yet (Attempt $ATTEMPT/$MAX_ATTEMPTS). Retrying in $SLEEP_BETWEEN sec..."
    sleep $SLEEP_BETWEEN
  done
}

###############################################################################
wait_for_flow_controller() {
  echo "[INFO] ---------------------------------------"
  echo "[INFO] Waiting for Flow Controller to finish initializing..."
  for ((ATTEMPT=1; ATTEMPT<=MAX_ATTEMPTS; ATTEMPT++)); do
    STATUS=$(curl -s -X GET "$NIFI_URL/nifi-api/flow/status")
    echo "[INFO] Checking => $STATUS"
    if ! echo "$STATUS" | grep -q "The Flow Controller is initializing the Data Flow."; then
      echo "[INFO] Flow Controller has finished initializing."
      return
    fi
    echo "[DEBUG] - Flow Controller still initializing... ($ATTEMPT/$MAX_ATTEMPTS)"
    sleep $SLEEP_BETWEEN
  done
  echo "[ERROR] - Flow Controller did not finish initialization in time."
  exit 1
}

###############################################################################
create_registry_client() {
  echo "[INFO] ---------------------------------------"
  echo "[INFO] Creating NiFi Registry Client if it doesn't exist..."
  REGISTRY_CLIENT_ID=$(curl -s "$NIFI_URL/nifi-api/flow/registries" | jq -r ".registries[] | select(.component.name==\"$REGISTRY_CLIENT_NAME\") | .id")

  if [ -n "$REGISTRY_CLIENT_ID" ]; then
    echo "[INFO] - Registry Client already exists (ID: $REGISTRY_CLIENT_ID)"
    return
  fi

  CREATE_JSON=$(cat <<EOF
{
  "revision": {
    "clientId": "nifi-init-script",
    "version": 0
  },
  "component": {
    "name": "$REGISTRY_CLIENT_NAME",
    "uri": "$REGISTRY_CLIENT_URL",
    "description": "Auto-created registry client"
  }
}
EOF
) 
  echo "[INFO] - URL: $NIFI_URL/nifi-api/controller/registry-clients"
  echo "[INFO] - DATA: $CREATE_JSON"

  for ((ATTEMPT=1; ATTEMPT<=MAX_ATTEMPTS; ATTEMPT++)); do
    
    RESPONSE=$(curl -s -X POST "$NIFI_URL/nifi-api/controller/registry-clients" -H "Content-Type: application/json" -d "$CREATE_JSON")
    # Cluster is unable to service request to change flow: Node nifi:8080 is currently connecting
    echo "[INFO] - RESPONSE: $RESPONSE"
    echo "[INFO] Checking response => $RESPONSE"
    if ! echo "$RESPONSE" | grep -q "is currently connecting"; then
      echo "[INFO] - Registry Client created successfully."
      return
    fi
    echo "[DEBUG] - Node is still connecting... ($ATTEMPT/$MAX_ATTEMPTS)"
    sleep $SLEEP_BETWEEN
  done
  echo "[ERROR] - Node is still in connecting state. Exiting"
  exit 1
}

###############################################################################
create_registry_bucket_if_not_exists() {
  echo "[INFO] ---------------------------------------"
  echo "[INFO] Ensuring NiFi Registry bucket '$REGISTRY_BUCKET_NAME' exists..."

  BUCKETS_JSON=$(curl -s -H "Accept: application/json" "$REGISTRY_CLIENT_URL-api/buckets")
  BUCKET_ID=$(echo "$BUCKETS_JSON" | jq -r ".[] | select(.name==\"$REGISTRY_BUCKET_NAME\") | .identifier")

  if [[ -n "$BUCKET_ID" ]]; then
    echo "[INFO] - Registry bucket already exists with ID: $BUCKET_ID"
    return
  fi

  echo "[INFO] - Bucket not found. Creating it now..."
  CREATE_BUCKET_PAYLOAD=$(cat <<EOF
{
  "name": "$REGISTRY_BUCKET_NAME",
  "description": "Auto-created bucket for $REGISTRY_BUCKET_NAME flow"
}
EOF
)

  RESPONSE=$(curl -s -X POST "$REGISTRY_CLIENT_URL-api/buckets" \
    -H "Content-Type: application/json" \
    -d "$CREATE_BUCKET_PAYLOAD")

  NEW_BUCKET_ID=$(echo "$RESPONSE" | jq -r '.identifier')

  if [[ -n "$NEW_BUCKET_ID" && "$NEW_BUCKET_ID" != "null" ]]; then
    echo "[INFO] - Bucket created successfully with ID: $NEW_BUCKET_ID"
  else
    echo "[ERROR] - Failed to create bucket. Response was:"
    echo "$RESPONSE"
    exit 1
  fi
}

###############################################################################
create_prometheus_reporting_task() {
  echo "[INFO] ---------------------------------------"
  echo "[INFO] Creating PrometheusReportingTask if it doesn't exist..."
  curl -s "$NIFI_URL/nifi-api/flow/reporting-tasks"
  echo ""
  EXISTING_TASK_ID=$(curl -s "$NIFI_URL/nifi-api/flow/reporting-tasks" | jq -r '.reportingTasks[] | select(.component.name == "PrometheusReportingTask") | .component.id')
  echo "[INFO] result: $EXISTING_TASK_ID"
  if [ -n "$EXISTING_TASK_ID" ]; then
    echo "[INFO] - PrometheusReportingTask already exists (ID: $EXISTING_TASK_ID)"
    return
  fi

  echo "[INFO] - Preparing JSON request..."
  CREATE_JSON=$(cat <<EOF
{
  "revision": { "version": 0 },
  "component": {
    "name": "PrometheusReportingTask",
    "type": "org.apache.nifi.reporting.prometheus.PrometheusReportingTask",
    "properties": {
      "prometheus-reporting-task-metrics-endpoint-port": "9094",
      "prometheus-reporting-task-instance-id": "nifi-1"
    }
  }
}
EOF
)

  echo "[INFO] - Creating Reporting Task controller..."
  RESPONSE=$(curl -s -X POST "$NIFI_URL/nifi-api/controller/reporting-tasks" \
    -H "Content-Type: application/json" -d "$CREATE_JSON")

  TASK_ID=$(echo "$RESPONSE" | jq -r '.component.id')
  ENABLE_JSON=$(cat <<EOF
{
  "revision": { "version": 1 },
  "component": {
    "id": "$TASK_ID",
    "state": "RUNNING"
  }
}
EOF
)

  echo "[INFO] - Enabling Reporting Task controller..."
  curl -s -X PUT "$NIFI_URL/nifi-api/reporting-tasks/$TASK_ID" -H "Content-Type: application/json" -d "$ENABLE_JSON"
  echo ""
  echo "[INFO] - PrometheusReportingTask enabled."
}

###############################################################################
upload_integrator_framework_flow() {
  echo "[INFO] Checking for Integrator Framework flow already pre-loaded into Registry..."
  echo "[INFO] - searching for Bucket..."
  BUCKET_ID=$(curl -s $NIFI_REGISTRY_URL/nifi-registry-api/buckets | jq -r '.[] | select(.name=="Integrator Framework") | .identifier')
  echo "[INFO] - found: $BUCKET_ID"
  echo "[INFO] - searching for existing Flow within bucket..."
  EXISTING_FLOW_IDs=$(curl -s "$NIFI_REGISTRY_URL/nifi-registry-api/buckets/$BUCKET_ID/flows" | \
   jq -r '.[] | select(.bucketName=="Integrator Framework") | .identifier' | head -n 1)

  if [ -n "$EXISTING_FLOW_IDs" ]; then
    echo "[INFO] - Flow already pre-loaded (ID: $EXISTING_FLOW_IDs)"
    return
  fi

  echo "[INFO] - No Flow loaded. Creating Registry Flow..."
  NEW_FLOW_IDENTIFIER=$(curl -s -X POST $NIFI_REGISTRY_URL/nifi-registry-api/buckets/$BUCKET_ID/flows -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json' --data-raw '{"name":"Integrator Framework","description":"Integrator Framework"}' | \
    jq -r '.identifier')
  echo "[INFO] - Created Registry Flow id: $NEW_FLOW_IDENTIFIER"

  echo "[INFO] - Importing Flow into Registry, using Bucket: $BUCKET_ID and Flow Identifier: $NEW_FLOW_IDENTIFIER"
  curl -s -X 'POST' "$NIFI_REGISTRY_URL/nifi-registry-api/buckets/$BUCKET_ID/flows/$NEW_FLOW_IDENTIFIER/versions/import" \
    -H 'Accept: application/json, text/plain, */*' \
    -H 'Content-Type: application/json' \
    -d @/opt/nifi/flow.json

  echo ""
  echo "[INFO] - Flow loaded successfully."
}
###############################################################################
instantiate_integrator_framework_flow() {
  echo "[INFO] Checking for Integrator Framework flow instance..."
  ROOT_PG_ID=$(curl -s "$NIFI_URL/nifi-api/process-groups/root" | jq -r '.id')
  echo "[INFO] - root process group: $ROOT_PG_ID"
  EXISTING_PG_ID=$(curl -s "$NIFI_URL/nifi-api/process-groups/$ROOT_PG_ID/process-groups" | \
    jq -r '.processGroups[] | select(.component.name | test("Integrator[ _]Framework.*")) | .component.id')
    #jq -r '.processGroups[] | select(.component.name=="Integrator_Framework (InstantX)") | .component.id')
    #jq -r '.processGroups[] | select(.component.name=="Integrator Framework") | .component.id')

  if [ -n "$EXISTING_PG_ID" ]; then
    echo "[INFO] - Flow already instantiated (ID: $EXISTING_PG_ID)"
    return
  fi

  echo "[INFO] No Process Group found. Instantiating Integrator Framework from Registry..."
  REGISTRY_CLIENT_ID=$(curl -s "$NIFI_URL/nifi-api/flow/registries" | jq -r ".registries[] | select(.component.name==\"$REGISTRY_CLIENT_NAME\") | .id")
  echo "[INFO] - Registry client id: $REGISTRY_CLIENT_ID"
  BUCKET_ID=$(curl -s $NIFI_REGISTRY_URL/nifi-registry-api/buckets | jq -r '.[] | select(.name=="Integrator Framework") | .identifier')
  echo "[INFO] - Bucket id: $BUCKET_ID"
  FLOW_ID=$(curl -s $NIFI_REGISTRY_URL/nifi-registry-api/buckets/$BUCKET_ID/flows | jq -r '.[0].identifier')
  echo "[INFO] - Flow id: $FLOW_ID"
  #LATEST_VERSION=$(curl -s $NIFI_REGISTRY_URL/nifi-registry-api/buckets/$BUCKET_ID/flows/$FLOW_ID/versions | jq -r '.[].version' | sort -nr | head -1)
  LATEST_VERSION=$(curl -s $NIFI_REGISTRY_URL/nifi-registry-api/flows/$FLOW_ID/versions | jq -r '.[].version' | sort -nr | head -1)
  echo "[INFO] - Latest version: $LATEST_VERSION"

  echo "[INFO] - preparing request..."
  #${
  #$  "versionControlInformation": {
  #$    "registryId": "$REGISTRY_CLIENT_ID",
  #$    "bucketId": "$BUCKET_ID",
  #$    "flowId": "$FLOW_ID",
  #$    "version": $LATEST_VERSION
  #$  },
  #$  "originX": 0.0,
  #$  "originY": 0.0
  #$}
  INSTANTIATE_JSON=$(cat <<EOF
{
    "revision": {
        "clientId": "$REGISTRY_CLIENT_ID",
        "version": 0
    },
    "component": {
        "position": {
            "x": 407,
            "y": 212.01171875
        },
        "versionControlInformation": {
            "registryId": "$REGISTRY_CLIENT_ID",
            "bucketId": "$BUCKET_ID",
            "flowId": "$FLOW_ID",
            "version": $LATEST_VERSION
        }
    }
}
EOF
)
  
  # Echo the request details
  echo "[INFO] - instantiating flow"
  echo " - URL: $NIFI_URL/nifi-api/process-groups/$ROOT_PG_ID/process-groups"
  echo " - Data: $INSTANTIATE_JSON"

  #curl -v "$NIFI_URL/nifi-api/process-groups/$ROOT_PG_ID/versioned-process-groups" \
  RESPONSE=$(curl -s "$NIFI_URL/nifi-api/process-groups/$ROOT_PG_ID/process-groups" \
    -H "Content-Type: application/json" -d "$INSTANTIATE_JSON")

  # Echo the response
  echo " - Response: $RESPONSE"

  echo "[INFO] Flow instantiated successfully."
}

###############################################################################
# 🚀 Execution Flow
###############################################################################

wait_for_nifi_ready
wait_for_flow_controller
create_registry_client
create_registry_bucket_if_not_exists
create_prometheus_reporting_task
upload_integrator_framework_flow
instantiate_integrator_framework_flow

echo "[SUCCESS] NiFi environment fully initialized."

