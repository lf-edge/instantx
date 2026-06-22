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

import Header from './components/Header'
import Hero from './components/Hero'
import ProtocolStrip from './components/ProtocolStrip'
import Architecture from './components/Architecture'
import Features from './components/Features'
import QuickStart from './components/QuickStart'
import Contribute from './components/Contribute'
import Footer from './components/Footer'

function App() {
  return (
    <>
      <a className="skip" href="#main">Skip to content</a>
      <Header />
      <main id="main">
        <span id="top"></span>
        <Hero />
        <ProtocolStrip />
        <Architecture />
        <Features />
        <QuickStart />
        <Contribute />
      </main>
      <Footer />
    </>
  )
}

export default App
