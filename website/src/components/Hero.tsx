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

import SystemDiagram from './SystemDiagram'
import { ArrowRightIcon, GitHubIcon } from './icons'

const strongMuted = { color: 'var(--muted)', fontWeight: 600 } as const

function Hero() {
  return (
    <section className="hero">
      <div className="wrap hero-grid">
        <div>
          <span className="eyebrow">Open-source edge broker</span>
          <h1>
            Move real-time data <span className="grad">across every protocol</span>, at the edge.
          </h1>
          <p className="sub">
            InstantX is an open-source edge-cloud broker for real-time data exchange. Built for V2X and
            beyond, it bridges <strong>MQTT, REST, AMQP and Kafka</strong> and routes events by{' '}
            <strong>geographic location</strong> — so road users, infrastructure and backend systems
            exchange only what's relevant to their area, safely and in real time.
          </p>
          <div className="hero-cta">
            <a className="btn btn-primary" href="#quickstart">
              <ArrowRightIcon /> Quick start
            </a>
            <a className="btn btn-ghost" href="https://github.com/lf-edge/instantx" target="_blank" rel="noopener">
              <GitHubIcon /> Star on GitHub
            </a>
          </div>
          <div className="hero-meta">
            <span>
              <span className="dot"></span> Apache-2.0 &amp; MIT · built in the open
            </span>
            <span>
              <span className="dot" style={{ background: 'var(--cyan)' }}></span> Self-hostable with Docker
            </span>
            <span>
              <span className="dot" style={{ background: 'var(--accent)' }}></span> Geohash pub/sub · ETSI &amp; 5GAA
            </span>
          </div>
          <p
            style={{
              marginTop: 20,
              fontSize: '13.5px',
              lineHeight: 1.5,
              color: 'var(--faint)',
              maxWidth: '52ch',
            }}
          >
            Developed by <strong style={strongMuted}>Vodafone Business</strong> within{' '}
            <strong style={strongMuted}>STEP</strong> (Safer Transport for Europe Platform), in
            collaboration with <strong style={strongMuted}>LF Edge</strong>.
          </p>
        </div>

        <SystemDiagram />
      </div>
    </section>
  )
}

export default Hero
