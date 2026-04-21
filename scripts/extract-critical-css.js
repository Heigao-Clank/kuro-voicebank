var fs = require('fs');
var path = require('path');

var ROOT = path.resolve(__dirname, '..');
var CSS_PATH = path.join(ROOT, 'style.css');
var HTML_FILES = ['index.html', 'index-en.html', 'index-jp.html'];

var css = fs.readFileSync(CSS_PATH, 'utf8');

// Selectors needed for above-the-fold (first screen):
// - CSS variables, reset, base body
// - Background decoration (bg-deco)
// - Sidebar (fixed, always visible on desktop)
// - Sidebar toggle + overlay (mobile)
// - Language switcher (fixed)
// - Main content layout
// - Container
// - Hero section + all sub-elements
// - Buttons (hero download buttons)
// - Media queries for hero/sidebar/lang-switcher
// - @font-face (local fonts)
// - .vb-type
// - @keyframes used by above (marquee-left, marquee-right, arc-pulse)
//
// NOT included: demo, profile, voicebank, download accordion,
//   guidelines, FAQ, contact, footer, protocol tabs — all below fold

var CRITICAL_PATTERNS = [
  // @font-face declarations
  /@font-face\s*\{[^}]+\}/g,
  // CSS variables and reset
  /:root\s*\{[^}]+\}/,
  /\*\s*\{[^}]+\}/,
  /html\s*\{[^}]+\}/,
  /body\s*\{[^}]+\}/,
  // General links (standalone `a` rule, not nested)
  /^a\s*\{[^}]+\}/m,
  /^a:hover\s*\{[^}]+\}/m,
  // Background decoration
  /\.bg-deco\s*\{[^}]+\}/,
  /\.bg-deco-wrapper\s*\{[^}]+\}/,
  /\.bg-deco-row\s*\{[^}]+\}/,
  /\.bg-deco-text\s*\{[^}]+\}/,
  /\.scroll-left\s*\{[^}]+\}/,
  /\.scroll-right\s*\{[^}]+\}/,
  /\.scroll-left-slow\s*\{[^}]+\}/,
  // Main content layout
  /\.main-content\s*\{[^}]+\}/,
  // Container
  /\.container\s*\{[^}]+\}/,
  // Sidebar
  /\.sidebar\s*\{[^}]+\}/,
  /\.sidebar-brand\s*\{[^}]+\}/,
  /\.sidebar-brand-link\s*\{[^}]+\}/,
  /\.sidebar-brand-link\s+img\s*\{[^}]+\}/,
  /\.sidebar-brand-text\s*\{[^}]+\}/,
  /\.sidebar-nav\s*\{[^}]+\}/,
  /\.sidebar-nav\s+a\s*\{[^}]+\}/,
  /\.sidebar-nav\s+a::before\s*\{[^}]+\}/,
  /\.sidebar-nav\s+a:hover\s*\{[^}]+\}/,
  /\.sidebar-nav\s+a:hover::before\s*\{[^}]+\}/,
  /\.sidebar-nav\s+a\.active\s*\{[^}]+\}/,
  /\.sidebar-nav\s+a\.active::before\s*\{[^}]+\}/,
  /\.sidebar-nav\s+a\s*>\s*\*\s*\{[^}]+\}/,
  /\.sidebar-nav\s+a\.active:hover\s*\{[^}]+\}/,
  /\.sidebar-nav-icon\s*\{[^}]+\}/,
  /\.sidebar-nav-text\s*\{[^}]+\}/,
  /\.sidebar-footer\s*\{[^}]+\}/,
  /\.sidebar-sns\s*\{[^}]+\}/,
  /\.sidebar-sns-link\s*\{[^}]+\}/,
  /\.sidebar-sns-link:hover\s*\{[^}]+\}/,
  /\.sidebar-site\s*\{[^}]+\}/,
  /\.sidebar-site:hover\s*\{[^}]+\}/,
  // Bilibili brand in sidebar
  /\.sidebar-sns-link\.bilibili\s*\{[^}]+\}/,
  /\.sidebar-sns-link\.bilibili:hover\s*\{[^}]+\}/,
  // Sidebar toggle (mobile)
  /\.sidebar-toggle\s*\{[^}]+\}/,
  /\.sidebar-toggle\s+span\s*\{[^}]+\}/,
  /\.sidebar-toggle\.active\s+span:nth-child\(1\)\s*\{[^}]+\}/,
  /\.sidebar-toggle\.active\s+span:nth-child\(2\)\s*\{[^}]+\}/,
  /\.sidebar-toggle\.active\s+span:nth-child\(3\)\s*\{[^}]+\}/,
  // Sidebar overlay (mobile)
  /\.sidebar-overlay\s*\{[^}]+\}/,
  // Hero section
  /\.hero\s*\{[^}]+\}/,
  /\.hero-waveform\s*\{[^}]+\}/,
  /\.hero-waveform\s+\.bar\s*\{[^}]+\}/,
  /\.hero-waveform\s+\.bar:nth-child\(\d+\)\s*\{[^}]+\}/g,
  /\.hero-visual\s*\{[^}]+\}/,
  /\.hero-visual::before\s*\{[^}]+\}/,
  /\.hero-visual::after\s*\{[^}]+\}/,
  /\.hero-visual\s+img\s*\{[^}]+\}/,
  /\.hero-character\s*\{[^}]+\}/,
  /\.hero-visual-text\s*\{[^}]+\}/,
  /\.hero-text\s*\{[^}]+\}/,
  /\.hero-title\s*\{[^}]+\}/,
  /\.hero-subtitle\s*\{[^}]+\}/,
  /\.hero-description\s*\{[^}]+\}/,
  /\.hero-download\s*\{[^}]+\}/,
  // vb-type
  /p\s+\.vb-type\s*,\s*\.voice-stat-value\s+\.vb-type\s*\{[^}]+\}/,
  // Buttons
  /\.btn\s*\{[^}]+\}/,
  /\.btn-primary\s*\{[^}]+\}/,
  /\.btn-primary:hover\s*\{[^}]+\}/,
  /\.btn-secondary\s*\{[^}]+\}/,
  /\.btn-secondary:hover\s*\{[^}]+\}/,
  /\.btn-warm\s*\{[^}]+\}/,
  /\.btn-warm:hover\s*\{[^}]+\}/,
  // Language switcher
  /\.lang-switcher\s*\{[^}]+\}/,
  /\.lang-switcher\s+a\s*\{[^}]+\}/,
  /\.lang-switcher\s+a:hover\s*\{[^}]+\}/,
  /\.lang-switcher\.hidden\s*\{[^}]+\}/,
  /\.lang-switcher\s+a\.active\s*\{[^}]+\}/,
  // Keyframes
  /@keyframes\s+marquee-left\s*\{[^}]+\{[^}]+\}[^}]+\}/,
  /@keyframes\s+marquee-right\s*\{[^}]+\{[^}]+\}[^}]+\}/,
  /@keyframes\s+arc-pulse\s*\{[^}]+\{[^}]+\}[^}]+\}/,
];

// For media queries, we need to match the whole block including nested rules
function extractMediaQuery(css, condition) {
  var idx = css.indexOf(condition);
  if (idx === -1) return '';

  // Find the opening brace
  var braceStart = css.indexOf('{', idx);
  var depth = 1;
  var pos = braceStart + 1;
  while (pos < css.length && depth > 0) {
    if (css[pos] === '{') depth++;
    else if (css[pos] === '}') depth--;
    pos++;
  }
  return css.substring(idx, pos);
}

// For @keyframes with nested braces, similar approach
function extractBlock(css, keyword) {
  var idx = css.indexOf(keyword);
  if (idx === -1) return '';
  var braceStart = css.indexOf('{', idx);
  var depth = 1;
  var pos = braceStart + 1;
  while (pos < css.length && depth > 0) {
    if (css[pos] === '{') depth++;
    else if (css[pos] === '}') depth--;
    pos++;
  }
  return css.substring(idx, pos);
}

var criticalParts = [];

CRITICAL_PATTERNS.forEach(function(pattern) {
  if (pattern.global) {
    var match;
    while ((match = pattern.exec(css)) !== null) {
      criticalParts.push(match[0]);
    }
  } else {
    var match = pattern.exec(css);
    if (match) criticalParts.push(match[0]);
  }
});

// Extract keyframes properly (nested braces)
['@keyframes marquee-left', '@keyframes marquee-right', '@keyframes arc-pulse'].forEach(function(kf) {
  var block = extractBlock(css, kf);
  if (block && criticalParts.indexOf(block) === -1) {
    criticalParts.push(block);
  }
});

// Extract responsive media queries for critical selectors
var mediaQueries = [
  '@media (min-width: 901px)',
  '@media (max-width: 900px)',
  '@media (max-width: 600px)'
];

mediaQueries.forEach(function(mq) {
  var block = extractMediaQuery(css, mq);
  if (block) {
    // Filter: only keep rules relevant to critical selectors
    var filteredBlock = filterMediaBlock(block);
    if (filteredBlock) criticalParts.push(filteredBlock);
  }
});

function filterMediaBlock(block) {
  var criticalSelectors = [
    '.sidebar', '.sidebar-toggle', '.sidebar-overlay', '.main-content',
    '.lang-switcher', '.hero', '.hero-visual', '.hero-character',
    '.hero-title', '.hero-waveform', '.hero-download',
    '.container', '.section', ':root', '.btn'
  ];

  var braceStart = block.indexOf('{');
  var header = block.substring(0, braceStart + 1);
  var inner = block.substring(braceStart + 1, block.length - 1);

  var rules = [];
  var pos = 0;
  while (pos < inner.length) {
    // Skip whitespace
    while (pos < inner.length && /\s/.test(inner[pos])) pos++;
    if (pos >= inner.length) break;

    // Find the rule start (selector)
    var ruleStart = pos;
    var braceIdx = inner.indexOf('{', pos);
    if (braceIdx === -1) break;

    var selector = inner.substring(ruleStart, braceIdx).trim();

    // Find matching closing brace
    var depth = 1;
    var rulePos = braceIdx + 1;
    while (rulePos < inner.length && depth > 0) {
      if (inner[rulePos] === '{') depth++;
      else if (inner[rulePos] === '}') depth--;
      rulePos++;
    }

    var fullRule = inner.substring(ruleStart, rulePos);

    // Check if this rule's selector is critical
    var isCritical = criticalSelectors.some(function(cs) {
      return selector.indexOf(cs) !== -1;
    });

    if (isCritical) {
      rules.push(fullRule);
    }

    pos = rulePos;
  }

  if (rules.length === 0) return '';
  return header + '\n  ' + rules.join('\n  ') + '\n}';
}

// Deduplicate
var seen = {};
var unique = [];
criticalParts.forEach(function(part) {
  var key = part.trim();
  if (!seen[key]) {
    seen[key] = true;
    unique.push(part.trim());
  }
});

// Reorder: @font-face first, then :root, then *, then rest
var fontFaces = [];
var rootVars = [];
var reset = [];
var rest = [];

unique.forEach(function(rule) {
  if (rule.indexOf('@font-face') === 0) fontFaces.push(rule);
  else if (rule.indexOf(':root') === 0) rootVars.push(rule);
  else if (rule.match(/^\*\s*\{/)) reset.push(rule);
  else rest.push(rule);
});

var criticalCSS = []
  .concat(fontFaces)
  .concat(rootVars)
  .concat(reset)
  .concat(rest)
  .join('\n\n');

// Minify the critical CSS (basic)
var miniCSS = criticalCSS
  .replace(/\/\*[\s\S]*?\*\//g, '')
  .replace(/\n\s*\n/g, '\n')
  .replace(/\s*\{\s*/g, '{')
  .replace(/\s*\}\s*/g, '}')
  .replace(/\s*;\s*/g, ';')
  .replace(/\s*:\s*/g, ':')
  .replace(/\s*,\s*/g, ',')
  .replace(/\s+/g, ' ')
  .trim();

console.log('Critical CSS extracted: ' + miniCSS.length + ' bytes (minified)');

// Now update each HTML file
HTML_FILES.forEach(function(file) {
  var htmlPath = path.join(ROOT, file);
  if (!fs.existsSync(htmlPath)) {
    console.log('SKIP: ' + file + ' not found');
    return;
  }

  var html = fs.readFileSync(htmlPath, 'utf8');

  // === Full cleanup of any previous critical CSS + async load artifacts ===
  // Remove <noscript><style id="critical-css">...</style></noscript> (bad wrap)
  html = html.replace(/<noscript>\s*<style id="critical-css">[\s\S]*?<\/style>\s*<\/noscript>/g, '');
  // Remove standalone <style id="critical-css">...</style>
  html = html.replace(/<style id="critical-css">[\s\S]*?<\/style>/g, '');
  // Remove <link rel="preload" ... style.css>
  html = html.replace(/<link[^>]*rel="preload"[^>]*href="style\.css"[^>]*\/?>/g, '');
  html = html.replace(/<link[^>]*href="style\.css"[^>]*rel="preload"[^>]*\/?>/g, '');
  // Remove <noscript><link ... style.css></noscript>
  html = html.replace(/<noscript><link[^>]*rel="stylesheet"[^>]*href="style\.css"[^>]*><\/noscript>/g, '');
  // Remove any stray empty <noscript></noscript>
  html = html.replace(/<noscript>\s*<\/noscript>/g, '');

  // Find the existing <link rel="stylesheet" href="style.css">
  var stylesheetLinkMatch = html.match(/<link[^>]*rel="stylesheet"[^>]*href="style\.css"[^>]*>/);

  if (stylesheetLinkMatch) {
    var replacement = '  <style id="critical-css">' + miniCSS + '</style>\n'
      + '  <link rel="preload" href="style.css" as="style" onload="this.rel=\'stylesheet\'">'
      + '<noscript><link rel="stylesheet" href="style.css"></noscript>';

    html = html.replace(stylesheetLinkMatch[0], replacement);
  } else {
    var block = '  <style id="critical-css">' + miniCSS + '</style>\n'
      + '  <link rel="preload" href="style.css" as="style" onload="this.rel=\'stylesheet\'">'
      + '<noscript><link rel="stylesheet" href="style.css"></noscript>\n';

    html = html.replace('</head>', block + '</head>');
  }

  fs.writeFileSync(htmlPath, html, 'utf8');
  console.log('Updated: ' + file);
});

console.log('Done! Run this script again after editing style.css.');
