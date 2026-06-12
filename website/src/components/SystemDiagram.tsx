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

// Inline SVG (not an <img>) so the diagram themes through the CSS custom
// properties referenced by the sm-* classes in global.css.
function SystemDiagram() {
  return (
    <div className="sysmap">
      <div className="sysmap-card">
        <div className="sysmap-head">
          <span className="t">System context</span>
          <span className="t2">how data moves</span>
        </div>
        <svg viewBox="0 0 600 600" role="img" aria-labelledby="smTitle smDesc">
          <title id="smTitle">InstantX system-context diagram</title>
          <desc id="smDesc">
            InstantX is the central edge data broker. An operational team views and manages activity
            dashboards. Devices within a GeoHash area publish and consume location-scoped events.
            External partner systems publish messages for distribution and receive message propagation.
          </desc>
          <defs>
            <marker id="smAh" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
              <path d="M0 0 L10 5 L0 10 z" className="sm-ah" />
            </marker>
          </defs>

          {/* edges (under nodes) */}
          <line className="sm-edge" x1="370" y1="118" x2="370" y2="238" markerEnd="url(#smAh)" />
          <line className="sm-edge" x1="168" y1="300" x2="261" y2="300" markerStart="url(#smAh)" markerEnd="url(#smAh)" />
          <line className="sm-edge" x1="370" y1="480" x2="370" y2="362" markerStart="url(#smAh)" markerEnd="url(#smAh)" />

          {/* edge labels */}
          <text className="sm-label" x="384" y="170">view / manage</text>
          <text className="sm-label-d" x="384" y="184">dashboards</text>
          <text className="sm-label" x="214" y="286" textAnchor="middle">publish · consume</text>
          <text className="sm-label-d" x="214" y="318" textAnchor="middle">by location</text>
          <text className="sm-label" x="384" y="408">publish ↑</text>
          <text className="sm-label-d" x="384" y="422">message propagation ↓</text>

          {/* GeoHash area node */}
          <rect className="sm-frame" x="14" y="222" width="150" height="150" rx="12" />
          <g className="sm-grid">
            <line x1="64" y1="222" x2="64" y2="372" />
            <line x1="114" y1="222" x2="114" y2="372" />
            <line x1="14" y1="272" x2="164" y2="272" />
            <line x1="14" y1="322" x2="164" y2="322" />
          </g>
          <rect className="sm-cell" x="64" y="272" width="50" height="50" rx="3" />
          <circle className="sm-pulse sm-ring" cx="89" cy="297" r="16" />
          <path className="sm-pin" d="M89 285 c-6 0 -10 4.4 -10 10 c0 7 10 16 10 16 c0 0 10 -9 10 -16 c0 -5.6 -4 -10 -10 -10 z" />
          <circle cx="89" cy="295" r="3.1" fill="var(--bg)" />
          {/* car */}
          <g className="sm-dev">
            <path d="M26 250 h26 M29 250 l2 -6 h12 l2 6" />
            <circle className="sm-dev-f" cx="33" cy="252" r="2.3" />
            <circle className="sm-dev-f" cx="46" cy="252" r="2.3" />
          </g>
          {/* roadside unit / signal */}
          <g className="sm-dev">
            <line x1="139" y1="244" x2="139" y2="256" />
            <path d="M132 244 a9 9 0 0 1 14 0" />
            <path d="M128 240 a14 14 0 0 1 22 0" />
          </g>
          {/* sensor broadcast */}
          <g className="sm-dev">
            <circle className="sm-dev-f" cx="39" cy="351" r="2.3" />
            <path d="M33 351 a8 8 0 0 1 12 0" />
            <path d="M30 347 a13 13 0 0 1 18 0" />
          </g>
          {/* edge node / chip */}
          <g className="sm-dev">
            <rect x="131" y="341" width="16" height="14" rx="2" />
            <line x1="135" y1="339" x2="135" y2="341" />
            <line x1="143" y1="339" x2="143" y2="341" />
            <line x1="135" y1="355" x2="135" y2="357" />
            <line x1="143" y1="355" x2="143" y2="357" />
          </g>
          <text className="sm-geo-title" x="89" y="392" textAnchor="middle">GeoHash area</text>
          <text className="sm-label-d" x="89" y="407" textAnchor="middle">vehicles · sensors · RSUs</text>

          {/* Operational team [Person] */}
          <circle className="sm-head" cx="370" cy="26" r="14" />
          <rect className="sm-box" x="268" y="34" width="204" height="84" rx="14" />
          <text className="sm-ntitle" x="370" y="70" textAnchor="middle">Operational team</text>
          <text className="sm-ntag" x="370" y="86" textAnchor="middle">[ PERSON ]</text>
          <text className="sm-nsub" x="370" y="104" textAnchor="middle">observability access</text>

          {/* InstantX core */}
          <rect className="sm-core" x="265" y="242" width="210" height="116" rx="16" />
          <text className="sm-core-tag" x="370" y="282" textAnchor="middle">EDGE DATA BROKER</text>
          <text className="sm-core-title" x="370" y="308" textAnchor="middle">InstantX</text>
          <text className="sm-core-sub" x="370" y="330" textAnchor="middle">geohash pub/sub · multi-protocol</text>

          {/* External systems */}
          <rect className="sm-box" x="268" y="484" width="204" height="88" rx="14" />
          <text className="sm-ntitle" x="370" y="518" textAnchor="middle">External systems</text>
          <text className="sm-ntag" x="370" y="534" textAnchor="middle">[ SOFTWARE SYSTEM ]</text>
          <text className="sm-nsub" x="370" y="552" textAnchor="middle">partner &amp; public data</text>
        </svg>
      </div>
      <p className="sysmap-cap">
        InstantX brokers location-scoped events between field devices, operators, and partner systems —
        a redrawn take on the project's{' '}
        <a href="https://github.com/lf-edge/instantx/blob/main/images/SystemContext.png" target="_blank" rel="noopener">
          C4 context diagram
        </a>
        .
      </p>
    </div>
  )
}

export default SystemDiagram
