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

const CARDS = [
  {
    href: 'https://github.com/lf-edge/instantx/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22',
    pill: 'Start here',
    title: 'Good first issues',
    body: 'Scoped, well-described tasks tagged for newcomers. The fastest way to land your first pull request.',
  },
  {
    href: 'https://github.com/lf-edge/instantx/blob/main/CONTRIBUTING.md',
    title: 'Contributing guide',
    body: 'Dev setup, branch conventions, coding standards and the review checklist — read this before your first PR.',
  },
  {
    href: 'https://github.com/lf-edge/instantx/discussions',
    title: 'Join the discussion',
    body: 'Propose a protocol, ask a question, or shape the roadmap with maintainers and other adopters.',
  },
  {
    href: 'https://github.com/lf-edge/instantx/issues/new/choose',
    title: 'Report a bug or idea',
    body: 'Found something off, or want a feature? Open an issue — reproductions and use-cases are gold.',
  },
  {
    href: 'https://github.com/lf-edge/instantx/blob/main/ROADMAP.md',
    title: 'Roadmap: now · next · later',
    body: 'See where InstantX is headed and where new message types and adapters fit — indicative, and shaped by community needs.',
  },
  {
    href: 'https://github.com/lf-edge/instantx/blob/main/CODE_OF_CONDUCT.md',
    title: 'Code of conduct',
    body: 'We keep the project welcoming and harassment-free. By participating you agree to uphold these standards.',
  },
]

const FLOW_STEPS = ['Fork', 'Branch', 'Commit', 'Open PR', 'Review', 'Merge']

function Contribute() {
  return (
    <section className="section contribute" id="contribute">
      <div className="wrap">
        <div className="section-head">
          <span className="eyebrow">Contribute</span>
          <h2>Built in the open — come build with us.</h2>
          <p>
            InstantX grows with its ecosystem: vehicle platforms, roadside infrastructure, and the backend
            systems that consume the data. Whether you fix a typo or add a new protocol adapter, there's an
            on-ramp for you.
          </p>
        </div>

        <div className="contrib-grid">
          {CARDS.map(({ href, pill, title, body }) => (
            <a key={href} className="ccard" href={href} target="_blank" rel="noopener">
              {pill && <span className="pill">{pill}</span>}
              <h3>
                {title} <span className="arrow">↗</span>
              </h3>
              <p>{body}</p>
            </a>
          ))}
        </div>

        <div className="flow" aria-label="Contribution workflow">
          <span className="flabel">PR flow</span>
          {FLOW_STEPS.map((step, i) => (
            <span key={step} style={{ display: 'contents' }}>
              <span className="fstep">
                <span className="n">{String(i + 1).padStart(2, '0')}</span> {step}
              </span>
              {i < FLOW_STEPS.length - 1 && <span className="fsep">→</span>}
            </span>
          ))}
        </div>
      </div>
    </section>
  )
}

export default Contribute
