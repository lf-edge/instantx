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

function Features() {
  return (
    <section
      className="section"
      id="features"
      style={{ background: 'var(--bg-2)', borderBlock: '1px solid var(--border)' }}
    >
      <div className="wrap">
        <div className="section-head">
          <span className="eyebrow">Capabilities</span>
          <h2>Built for interoperability, from the protocol up.</h2>
          <p>
            Location-aware pub/sub, multiple publishing paths and a standards-based core — with the whole
            stack self-hostable from a single <code>docker-compose up</code>.
          </p>
        </div>
        <div className="feat-grid">
          <article className="feat lead-card">
            <div className="ficon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Z" />
                <circle cx="12" cy="10" r="2.6" />
              </svg>
            </div>
            <h3>Geohash-based publish / subscribe</h3>
            <p>
              The signature pattern: events are tagged to a geographic cell, and subscribers receive only
              the messages relevant to their area. Asynchronous, location-aware data sharing made for road
              users in motion.
            </p>
            <div className="protos"><span>geohash</span><span>pub/sub</span></div>
          </article>
          <article className="feat lead-card">
            <div className="ficon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <path d="M12 3a9 9 0 1 0 9 9" />
                <path d="M12 8a4 4 0 1 0 4 4" />
                <circle cx="12" cy="12" r="1.4" fill="currentColor" />
              </svg>
            </div>
            <h3>Interoperability at a glance</h3>
            <p>
              Seamless compatibility across MQTT, REST, AMQP and Kafka means InstantX drops into existing
              backends instead of forcing a rewrite. Pick the protocol your systems already speak.
            </p>
            <div className="protos"><span>MQTT</span><span>REST</span><span>AMQP</span><span>Kafka</span></div>
          </article>

          <article className="feat">
            <div className="ficon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <path d="M5 8a7 7 0 0 1 14 0M8 12a3.5 3.5 0 0 1 8 0M12 16v.01" />
              </svg>
            </div>
            <h3>MQTT broker integration</h3>
            <p>Efficient, bi-directional, event-driven messaging at scale, powered by MQTT.</p>
            <div className="protos"><span>MQTT</span><span>:1883</span></div>
          </article>
          <article className="feat">
            <div className="ficon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <path d="M4 6h16v12H4z" />
                <path d="M4 10h16M8 6v12" />
              </svg>
            </div>
            <h3>HTTP REST API with OpenAPI</h3>
            <p>
              A friendly REST API for message publishing — the Event-Publisher service — fully documented
              with an OpenAPI specification.
            </p>
            <div className="protos"><span>REST</span><span>OpenAPI</span><span>:5000</span></div>
          </article>
          <article className="feat">
            <div className="ficon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <rect x="3" y="4" width="7" height="7" rx="1.5" />
                <rect x="14" y="13" width="7" height="7" rx="1.5" />
                <path d="M10 7.5h2a2 2 0 0 1 2 2V13" />
              </svg>
            </div>
            <h3>System-to-system integration</h3>
            <p>Robust platform-to-platform connectivity over AMQP — a third publishing path for backend pipelines.</p>
            <div className="protos"><span>AMQP</span></div>
          </article>
          <article className="feat">
            <div className="ficon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <path d="M4 7h16M4 12h16M4 17h10" />
                <circle cx="18" cy="17" r="2.4" />
              </svg>
            </div>
            <h3>Apache NiFi flow pipelines</h3>
            <p>
              Visual, configurable transformation flows built on Apache NiFi handle any message type
              through flexible APIs — adapt to new schemas without a rewrite.
            </p>
            <div className="protos"><span>Apache NiFi</span><span>flexible-apis</span></div>
          </article>
          <article className="feat">
            <div className="ficon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <path d="M4 19V5M4 19h16" />
                <path d="M8 16l3-4 3 2 4-6" />
              </svg>
            </div>
            <h3>Observability built in</h3>
            <p>
              Grafana dashboards ship with the stack — watch throughput, topics and message flow from the
              first <code>docker-compose up</code>.
            </p>
            <div className="protos"><span>Grafana</span><span>:3000</span></div>
          </article>
          <article className="feat">
            <div className="ficon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <path d="M12 3 4 6v6c0 4 3.5 7 8 9 4.5-2 8-5 8-9V6l-8-3Z" />
                <path d="M9 12l2 2 4-4" />
              </svg>
            </div>
            <h3>ETSI &amp; 5GAA standards</h3>
            <p>
              Full support for DENM messages using ASN.1 UPER encoding, aligned with ETSI and 5GAA for
              interoperability and compliance.
            </p>
            <a
              className="soon"
              style={{ marginTop: 'auto' }}
              href="https://github.com/lf-edge/instantx/blob/main/ROADMAP.md"
              target="_blank"
              rel="noopener"
            >
              Roadmap: now · next · later ↗
            </a>
          </article>
        </div>
      </div>
    </section>
  )
}

export default Features
