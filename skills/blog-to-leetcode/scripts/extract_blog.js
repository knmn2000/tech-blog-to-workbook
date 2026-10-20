// Reads a blog post's content in document order. Run it in the browser pane with the
// JavaScript tool, on the post's page. It stores everything in window.__blog and returns a
// compact outline (headings, and each code block's caption, language and size), so a long post
// doesn't flood the conversation. Fetch details afterwards, in slices, e.g.:
//   JSON.stringify(window.__blog.blocks.slice(0, 40))
//   window.__blog.blocks.filter(b => b.type === 'code').map(b => b.text)[3]
(() => {
  const root =
    document.querySelector('article') ||
    document.querySelector('main') ||
    document.querySelector('[role="main"]') ||
    document.body;
  const skip = (el) => el.closest('nav, footer, aside, header:not(article header), script, style, noscript');
  const clean = (s) => (s || '').replace(/\s+/g, ' ').trim();

  const languageOf = (pre) => {
    const code = pre.querySelector('code');
    const attrs = [pre.getAttribute('data-language'), code && code.getAttribute('data-language'),
                   pre.className, code && code.className].filter(Boolean).join(' ');
    const m = attrs.match(/(?:language-|lang-)?\b(cpp|c\+\+|c|rust|go|python|py|javascript|js|typescript|ts|java|kotlin|swift|csharp|cs|ruby|php|scala|haskell|sql|bash|sh|shell|zsh|powershell|json|yaml|toml|glsl|hlsl|wgsl|asm|zig|lua|elixir|ocaml|text|plaintext)\b/i);
    return m ? m[1].toLowerCase() : '';
  };

  const captionOf = (pre) => {
    const fig = pre.closest('figure');
    if (fig && fig.querySelector('figcaption')) return clean(fig.querySelector('figcaption').innerText);
    for (const el of [pre, pre.parentElement, pre.parentElement && pre.parentElement.parentElement]) {
      if (!el) continue;
      for (const a of ['data-title', 'title', 'data-filename', 'data-rehype-pretty-code-title']) {
        if (el.getAttribute && el.getAttribute(a)) return clean(el.getAttribute(a));
      }
      const header = el.querySelector && el.querySelector(':scope > .code-title, :scope > .filename, :scope > [class*="title"], :scope > [class*="filename"]');
      if (header && header !== pre && clean(header.innerText).length < 120) return clean(header.innerText);
    }
    // A short paragraph right before the block, all bold or ending in ':' or naming a file.
    let prev = pre.previousElementSibling;
    if (!prev && pre.parentElement) prev = pre.parentElement.previousElementSibling;
    if (prev) {
      const text = clean(prev.innerText);
      const strong = prev.querySelector('strong, b');
      const allBold = strong && clean(strong.innerText) === text;
      if (text && text.length <= 120 && (allBold || /:$/.test(text) || /\b[\w-]+\.\w{1,5}\b/.test(text))) return text;
    }
    return '';
  };

  const blocks = [];
  const seen = new Set();
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
  for (let el = walker.currentNode; el; el = walker.nextNode()) {
    if (seen.has(el) || skip(el)) continue;
    const tag = el.tagName;
    if (/^H[1-4]$/.test(tag)) {
      blocks.push({ type: 'heading', level: Number(tag[1]), text: clean(el.innerText), id: el.id || '' });
    } else if (tag === 'PRE') {
      const text = el.innerText.replace(/\s+$/, '');
      blocks.push({ type: 'code', caption: captionOf(el), lang: languageOf(el), lines: text.split('\n').length, text });
      el.querySelectorAll('*').forEach((c) => seen.add(c));
    } else if (tag === 'P' || tag === 'BLOCKQUOTE') {
      const text = clean(el.innerText);
      if (text) blocks.push({ type: 'text', text });
      el.querySelectorAll('*').forEach((c) => seen.add(c));
    } else if (tag === 'LI' && !el.querySelector('p')) {
      const text = clean(el.innerText);
      if (text) blocks.push({ type: 'item', text });
      el.querySelectorAll('*').forEach((c) => seen.add(c));
    } else if (tag === 'TABLE') {
      const rows = [...el.querySelectorAll('tr')].map((tr) => [...tr.children].map((td) => clean(td.innerText)));
      blocks.push({ type: 'table', rows });
      el.querySelectorAll('*').forEach((c) => seen.add(c));
    } else if (tag === 'IMG') {
      blocks.push({ type: 'image', alt: el.alt || '', src: el.currentSrc || el.src });
    } else if (el.classList && (el.classList.contains('katex-display') || tag === 'MATH')) {
      blocks.push({ type: 'math', text: clean(el.innerText) });
      el.querySelectorAll('*').forEach((c) => seen.add(c));
    }
  }

  window.__blog = { url: location.href, title: document.title, blocks };
  const code = blocks.filter((b) => b.type === 'code');
  return {
    url: location.href,
    title: document.title,
    blocks: blocks.length,
    codeBlocks: code.length,
    codeLines: code.reduce((n, b) => n + b.lines, 0),
    outline: blocks
      .map((b, i) => b.type === 'heading' ? `#${i} ${'#'.repeat(b.level)} ${b.text}` :
                     b.type === 'code' ? `#${i}   [code ${b.lang || '?'} ${b.lines} lines] ${b.caption}` : null)
      .filter(Boolean),
  };
})();
