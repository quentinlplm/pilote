// Pilote s'ouvre même sans réseau : la page et ses icônes sont gardées sur le téléphone.
// La page passe toujours par le réseau d'abord, pour qu'une nouvelle version arrive dès le lancement suivant.
// Les données, elles, ne sont jamais mises en cache ici : l'app garde sa propre copie.
const CACHE = "pilote-ami-c728-v1";
const COQUILLE = ["./", "./manifest.webmanifest", "../icones/icone-180.png", "../icones/icone-192.png", "../icones/icone-512.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(COQUILLE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((cles) => Promise.all(cles.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;
  e.respondWith(
    fetch(e.request)
      .then((r) => {
        if (r.ok) { const copie = r.clone(); caches.open(CACHE).then((c) => c.put(e.request, copie)); }
        return r;
      })
      .catch(() => caches.match(e.request).then((r) => r || caches.match("./")))
  );
});
