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

import CopyButton from './CopyButton'
import Tabs from './Tabs'

const DOCKER_COPY = 'git clone https://github.com/lf-edge/instantx.git\ncd instantx\ndocker-compose up -d'
const SOURCE_COPY = 'git clone https://github.com/lf-edge/instantx.git\ncd instantx\ndocker-compose up --build -d'

// Whitespace inside <pre> is explicit ({'\n'} strings) because JSX collapses
// literal newlines between elements.
const dockerPanel = (
  <div className="code-block">
    <CopyButton text={DOCKER_COPY} label="Copy Docker commands" />
    <pre>
      <code>
        <span className="cm"># clone &amp; enter</span>
        {'\n'}
        <span className="pr">$ </span>
        {'git clone https://github.com/lf-edge/instantx.git\n'}
        <span className="pr">$ </span>
        {'cd instantx\n\n'}
        <span className="cm"># bring the whole stack up</span>
        {'\n'}
        <span className="pr">$ </span>
        {'docker-compose up '}
        <span className="arg">-d</span>
        {'\n\n'}
        <span className="cm"># mqtt :1883 · rest :5000</span>
        {'\n'}
        <span className="cm"># kafka :9092 · grafana :3000</span>
      </code>
    </pre>
  </div>
)

const sourcePanel = (
  <div className="code-block">
    <CopyButton text={SOURCE_COPY} label="Copy rebuild commands" />
    <pre>
      <code>
        <span className="cm"># InstantX is Python · rebuild after API changes</span>
        {'\n'}
        <span className="pr">$ </span>
        {'git clone https://github.com/lf-edge/instantx.git\n'}
        <span className="pr">$ </span>
        {'cd instantx\n\n'}
        <span className="cm"># rebuild the API service &amp; restart</span>
        {'\n'}
        <span className="pr">$ </span>
        {'docker-compose up '}
        <span className="arg">--build -d</span>
      </code>
    </pre>
  </div>
)

const QUICKSTART_TABS = [
  {
    id: 'docker',
    label: (
      <>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
          <path d="M4 11h14v3a4 4 0 0 1-4 4H9a5 5 0 0 1-5-5v-2Z" />
          <path d="M6 11V8h3v3M9 8V5h3v3M12 11V8h3v3" />
        </svg>
        Docker
      </>
    ),
    panel: dockerPanel,
  },
  {
    id: 'source',
    label: (
      <>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
          <path d="M9 7 4 12l5 5M15 7l5 5-5 5" />
        </svg>
        Dev rebuild
      </>
    ),
    panel: sourcePanel,
  },
]

function QuickStart() {
  return (
    <section className="section" id="quickstart">
      <div className="wrap">
        <div className="section-head">
          <span className="eyebrow">Quick start</span>
          <h2>Running locally in two commands.</h2>
          <p>Clone the repository and bring the broker up with Docker — no manual dependency wrangling.</p>
        </div>
        <div className="qs-grid">
          <ol className="qs-steps">
            <li>
              <div>
                <h3>Clone the repository</h3>
                <p>Grab the source from GitHub and step into the project directory.</p>
              </div>
            </li>
            <li>
              <div>
                <h3>Start the stack</h3>
                <p>Compose spins up the MQTT broker, Kafka, NiFi and Grafana in one shot.</p>
              </div>
            </li>
            <li>
              <div>
                <h3>Publish your first message</h3>
                <p>
                  Hit the REST API on <code>:5000</code> or connect an MQTT client on <code>:1883</code>{' '}
                  and watch it route by geohash.
                </p>
              </div>
            </li>
          </ol>

          <Tabs tabs={QUICKSTART_TABS} ariaLabel="Quick start method" />
        </div>
      </div>
    </section>
  )
}

export default QuickStart
