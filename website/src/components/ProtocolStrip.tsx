/* ========================LICENSE_START=================================
 * InstantX Website
 * %%
 * Copyright (C) 2024 - 2026 Vodafone
 * %%
 * Licensed under the MIT License;
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      https://opensource.org/license/mit
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =========================LICENSE_END==================================
 */

function ProtocolStrip() {
  return (
    <section className="protocols" aria-label="Supported protocols">
      <div className="wrap">
        <span className="label">Speaks</span>
        <div className="proto-list">
          <span className="proto"><b>MQTT</b> broker</span>
          <span className="proto"><b>HTTP REST</b> + OpenAPI</span>
          <span className="proto"><b>AMQP</b> system-to-system</span>
          <span className="proto"><b>Apache Kafka</b> + Connect</span>
          <span className="proto"><b>ETSI DENM</b> · ASN.1 UPER</span>
          <span className="proto"><b>5GAA</b> aligned</span>
        </div>
      </div>
    </section>
  )
}

export default ProtocolStrip
