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

import { useEffect, useRef, useState } from 'react'
import { CheckIcon, CopyIcon } from './icons'

interface CopyButtonProps {
  text: string
  label: string
}

function fallbackCopy(value: string) {
  const ta = document.createElement('textarea')
  ta.value = value
  ta.style.position = 'fixed'
  ta.style.opacity = '0'
  document.body.appendChild(ta)
  ta.focus()
  ta.select()
  try {
    document.execCommand('copy')
  } catch {
    // clipboard unavailable — nothing else to try
  }
  document.body.removeChild(ta)
}

function CopyButton({ text, label }: CopyButtonProps) {
  const [copied, setCopied] = useState(false)
  const timer = useRef<number | undefined>(undefined)

  useEffect(() => () => window.clearTimeout(timer.current), [])

  function handleClick() {
    const done = () => {
      setCopied(true)
      window.clearTimeout(timer.current)
      timer.current = window.setTimeout(() => setCopied(false), 1800)
    }
    if (navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(text).then(done, () => {
        fallbackCopy(text)
        done()
      })
    } else {
      fallbackCopy(text)
      done()
    }
  }

  return (
    <button className={`copy-btn${copied ? ' copied' : ''}`} onClick={handleClick} aria-label={label}>
      {copied ? (
        <>
          <CheckIcon /> Copied
        </>
      ) : (
        <>
          <CopyIcon /> Copy
        </>
      )}
    </button>
  )
}

export default CopyButton
