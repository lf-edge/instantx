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

import { ArrowRightIcon } from './icons'

function Architecture() {
  return (
    <section className="section" id="architecture">
      <div className="wrap">
        <div className="section-head">
          <span className="eyebrow">How it works</span>
          <h2>One edge node between the road and your backend.</h2>
          <p>
            InstantX ingests messages over any supported protocol, transforms them through configurable
            pipelines, and routes them to wherever they need to go — no vendor lock-in, no format mismatch.
          </p>
        </div>

        <figure style={{ margin: 0 }}>
          <div className="arch-flow">
            <div className="arch-col">
              <svg className="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true">
                <path d="M3 17h2l1-5h12l1 5h2" />
                <path d="M6 17a2 2 0 1 0 4 0M14 17a2 2 0 1 0 4 0" />
                <path d="M7 12 8 8h8l1 4" />
              </svg>
              <span className="kind">Source</span>
              <h3>Road users &amp; infrastructure</h3>
              <ul>
                <li>Vehicles &amp; V2X units</li>
                <li>Roadside sensors</li>
                <li>IIoT &amp; field devices</li>
              </ul>
              <ArrowRightIcon className="arch-arrow" />
            </div>
            <div className="arch-col">
              <svg className="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true">
                <path d="M12 3v6M12 15v6M3 12h6M15 12h6" />
                <circle cx="12" cy="12" r="3" />
              </svg>
              <span className="kind">Ingest</span>
              <h3>Multi-protocol intake</h3>
              <ul>
                <li>MQTT subscribe/publish</li>
                <li>REST + OpenAPI</li>
                <li>AMQP endpoints</li>
              </ul>
              <ArrowRightIcon className="arch-arrow" />
            </div>
            <div className="arch-col core">
              <svg className="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true">
                <rect x="3" y="4" width="18" height="16" rx="2" />
                <path d="M3 9h18M8 14l2 2 4-4" />
              </svg>
              <span className="kind">InstantX core</span>
              <h3>Transform &amp; route</h3>
              <ul>
                <li>Decode ETSI / ASN.1 UPER</li>
                <li>Geohash pub/sub routing</li>
                <li>Apache NiFi flow pipelines</li>
              </ul>
              <ArrowRightIcon className="arch-arrow" />
            </div>
            <div className="arch-col">
              <svg className="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true">
                <path d="M4 6h16M4 12h16M4 18h10" />
              </svg>
              <span className="kind">Deliver</span>
              <h3>Backends &amp; operators</h3>
              <ul>
                <li>Kafka + Kafka Connect</li>
                <li>External systems</li>
                <li>Grafana dashboards</li>
              </ul>
            </div>
          </div>
          <figcaption className="arch-note">
            <b>Standards-first:</b>
            <span>DENM safety messages are decoded with</span>
            <span className="tag">ASN.1 UPER</span>
            <span>aligned to ETSI &amp; 5GAA, then routed by</span>
            <span className="tag">geohash</span>
            <span>so subscribers receive only what's relevant to their area.</span>
          </figcaption>
        </figure>
      </div>
    </section>
  )
}

export default Architecture
