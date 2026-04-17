// Local Lucide-style icon loader
(function() {
  const icons = {};
  
  // Load all icons from local SVG files
  function loadIcon(name, svg) {
    icons[name] = svg;
  }
  
  // Preload icons
  const iconFiles = [
    'assets/icons/book-open.svg',
    'assets/icons/cake.svg',
    'assets/icons/check.svg',
    'assets/icons/download.svg',
    'assets/icons/heart.svg',
    'assets/icons/help-circle.svg',
    'assets/icons/home.svg',
    'assets/icons/mail.svg',
    'assets/icons/mic.svg',
    'assets/icons/paw-print.svg',
    'assets/icons/ruler.svg',
    'assets/icons/sparkles.svg',
    'assets/icons/tv.svg',
    'assets/icons/user.svg',
    'assets/icons/x.svg'
  ];
  
  Promise.all(iconFiles.map(function(file) {
    return fetch(file)
      .then(function(resp) { return resp.text(); })
      .then(function(svg) {
        var name = file.replace('assets/icons/', '').replace('.svg', '');
        loadIcon(name, svg);
      });
  })).then(function() {
    // Replace all icon elements
    document.querySelectorAll('i[data-lucide]').forEach(function(el) {
      var name = el.getAttribute('data-lucide');
      var style = el.getAttribute('style') || '';
      var className = el.getAttribute('class') || '';
      
      if (icons[name]) {
        var parser = new DOMParser();
        var svgDoc = parser.parseFromString(icons[name], 'image/svg+xml');
        var svgEl = svgDoc.documentElement;
        
        // Extract width/height from style if present
        var widthMatch = style.match(/width:\s*(\d+)px/);
        var heightMatch = style.match(/height:\s*(\d+)px/);
        
        if (widthMatch) svgEl.setAttribute('width', widthMatch[1]);
        if (heightMatch) svgEl.setAttribute('height', heightMatch[1]);
        
        svgEl.removeAttribute('xmlns');
        svgEl.setAttribute('class', className);
        if (style) svgEl.setAttribute('style', style);
        
        el.parentNode.replaceChild(svgEl, el);
      }
    });
  });
})();
