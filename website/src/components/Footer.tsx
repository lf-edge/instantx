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

import logoDark from '../assets/instantx-logo-dark.png'
import logoLight from '../assets/instantx-logo.png'
import { GitHubIcon } from './icons'

function Footer() {
  return (
    <footer className="site-footer" id="docs">
      <div className="wrap">
        <div className="footer-top">
          <div className="footer-brand">
            <a className="brand" href="#top" aria-label="InstantX home">
              <img className="brand-logo brand-logo--dark" src={logoDark} width={780} height={192} alt="" />
              <img className="brand-logo brand-logo--light" src={logoLight} width={780} height={192} alt="" />
            </a>
            <p>
              An open-source edge-cloud broker for real-time data exchange — V2X and beyond. Developed by
              Vodafone Business within STEP, in collaboration with LF Edge.
            </p>
          </div>
          <div className="fcol">
            <h4>Product</h4>
            <a href="#features">Features</a>
            <a href="#architecture">Architecture</a>
            <a href="#quickstart">Quick start</a>
          </div>
          <div className="fcol">
            <h4>Docs</h4>
            <a href="https://github.com/lf-edge/instantx/blob/main/deployment/Quick-Start.md" target="_blank" rel="noopener">Deployment quick-start</a>
            <a href="https://github.com/lf-edge/instantx/blob/main/docs/Development.md" target="_blank" rel="noopener">Development guide</a>
            <a href="https://github.com/lf-edge/instantx/blob/main/docs/MQTT-Topic-Structure.md" target="_blank" rel="noopener">MQTT topic structure</a>
            <a href="https://github.com/lf-edge/instantx/blob/main/docs/v2x-messages.md" target="_blank" rel="noopener">V2X message standards</a>
            <a href="https://github.com/lf-edge/instantx/blob/main/docs/Encoding.md" target="_blank" rel="noopener">UPER encoding</a>
          </div>
          <div className="fcol">
            <h4>Develop</h4>
            <a href="https://github.com/lf-edge/instantx" target="_blank" rel="noopener">GitHub repo</a>
            <a href="https://github.com/lf-edge/instantx/issues" target="_blank" rel="noopener">Issues</a>
            <a href="https://github.com/lf-edge/instantx/releases" target="_blank" rel="noopener">Releases · v2.1.0</a>
            <a href="https://github.com/lf-edge/instantx/wiki" target="_blank" rel="noopener">Wiki</a>
          </div>
          <div className="fcol">
            <h4>Community</h4>
            <a href="https://github.com/lf-edge/instantx/discussions" target="_blank" rel="noopener">Discussions</a>
            <a href="https://github.com/lf-edge/instantx/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener">Contributing</a>
            <a href="https://github.com/lf-edge/instantx/blob/main/CODE_OF_CONDUCT.md" target="_blank" rel="noopener">Code of conduct</a>
            <a href="https://github.com/lf-edge/instantx/blob/main/LICENSE.md" target="_blank" rel="noopener">License · MIT + Apache-2.0</a>
          </div>
        </div>
        <div className="footer-bottom">
          <span>© 2026 InstantX contributors · A Vodafone Business / STEP project, in collaboration with LF Edge</span>
          <span className="socials">
            <a className="icon-btn" href="https://github.com/lf-edge/instantx" target="_blank" rel="noopener" aria-label="InstantX on GitHub">
              <GitHubIcon />
            </a>
          </span>
        </div>
      </div>
    </footer>
  )
}

export default Footer
