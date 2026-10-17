// Minimal emulation of KSvg FrameSvg for previews: render an element by id
// (bounds = element bbox, stretched into target rect) and 9-slice frames.
window.__errors = [];
window.addEventListener('error', e => window.__errors.push(String(e.message)));
const SVGS = {};
function mountSvg(name, text) {
  text = text.replace(/id="([^"]+)"/g, (m, id) => `id="${name}__${id}"`)
             .replace(/url\(#([^)]+)\)/g, (m, id) => `url(#${name}__${id})`);
  const holder = document.createElement('div');
  holder.style.cssText = 'position:absolute;left:-20000px;top:0;';
  holder.innerHTML = text;
  document.body.appendChild(holder);
  SVGS[name] = holder;
}
function bb(name, id) {
  const el = document.getElementById(name + '__' + id);
  if (!el) return null;
  return el.getBBox();
}
function elem(name, id, x, y, w, h) {
  const b = bb(name, id);
  if (!b) { return ''; }
  return `<svg style="position:absolute;left:${x}px;top:${y}px;overflow:hidden" width="${w}" height="${h}" viewBox="${b.x} ${b.y} ${b.width} ${b.height}" preserveAspectRatio="none"><use href="#${name}__${id}"/></svg>`;
}
// borders: object {top,bottom,left,right} booleans (enabled borders)
function frame(name, prefix, x, y, W, H, borders) {
  borders = borders || {top: true, bottom: true, left: true, right: true};
  const p = prefix ? prefix + '-' : '';
  const g = n => bb(name, p + n);
  if (!g('center')) { window.__errors.push('missing ' + name + ':' + p + 'center'); return ''; }
  const L = borders.left && g('left') ? g('left').width : 0;
  const R = borders.right && g('right') ? g('right').width : 0;
  const T = borders.top && g('top') ? g('top').height : 0;
  const B = borders.bottom && g('bottom') ? g('bottom').height : 0;
  let s = `<div style="position:absolute;left:${x}px;top:${y}px;width:${W}px;height:${H}px">`;
  const mw = W - L - R, mh = H - T - B;
  s += elem(name, p + 'center', L, T, mw, mh);
  if (T) s += elem(name, p + 'top', L, 0, mw, T);
  if (B) s += elem(name, p + 'bottom', L, H - B, mw, B);
  if (L) s += elem(name, p + 'left', 0, T, L, mh);
  if (R) s += elem(name, p + 'right', W - R, T, R, mh);
  if (T && L) s += elem(name, p + 'topleft', 0, 0, L, T);
  if (T && R) s += elem(name, p + 'topright', W - R, 0, R, T);
  if (B && L) s += elem(name, p + 'bottomleft', 0, H - B, L, B);
  if (B && R) s += elem(name, p + 'bottomright', W - R, H - B, R, B);
  return s + '</div>';
}
