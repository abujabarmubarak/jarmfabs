/**
 * JarmFabs Technologies — Main Frontend Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Drawer Navigation
  const burger = document.getElementById('navBurger');
  const drawer = document.getElementById('mobileDrawer');
  const drawerClose = document.getElementById('drawerClose');
  const drawerBackdrop = document.getElementById('drawerBackdrop');

  function openDrawer() {
    if (drawer) {
      drawer.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeDrawer() {
    if (drawer) {
      drawer.classList.remove('open');
      document.body.style.overflow = '';
    }
  }

  if (burger) burger.addEventListener('click', openDrawer);
  if (drawerClose) drawerClose.addEventListener('click', closeDrawer);
  if (drawerBackdrop) drawerBackdrop.addEventListener('click', closeDrawer);

  document.querySelectorAll('.drawer-link').forEach(link => {
    link.addEventListener('click', closeDrawer);
  });

  // 2. Scroll effect on Navbar
  const siteNav = document.getElementById('siteNav');
  if (siteNav) {
    window.addEventListener('scroll', () => {
      siteNav.classList.toggle('scrolled', window.scrollY > 30);
    }, { passive: true });
  }

  // 3. Photo Gallery Filter & Lightbox
  const filterBtns = document.querySelectorAll('.gallery-filter-btn');
  const galleryCards = document.querySelectorAll('.gallery-card');
  const lightbox = document.getElementById('galleryLightbox');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxTitle = document.getElementById('lightboxTitle');
  const lightboxCaption = document.getElementById('lightboxCaption');
  const lightboxClose = document.getElementById('lightboxClose');

  if (filterBtns.length > 0 && galleryCards.length > 0) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const cat = btn.getAttribute('data-category');
        galleryCards.forEach(card => {
          if (cat === 'All' || card.getAttribute('data-category') === cat) {
            card.style.display = 'block';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  if (galleryCards.length > 0 && lightbox) {
    galleryCards.forEach(card => {
      card.addEventListener('click', () => {
        const src = card.getAttribute('data-img-src');
        const title = card.getAttribute('data-title');
        const caption = card.getAttribute('data-caption');

        if (lightboxImg) lightboxImg.src = src;
        if (lightboxTitle) lightboxTitle.textContent = title || '';
        if (lightboxCaption) lightboxCaption.textContent = caption || '';

        lightbox.classList.add('open');
        document.body.style.overflow = 'hidden';
      });
    });

    if (lightboxClose) {
      lightboxClose.addEventListener('click', () => {
        lightbox.classList.remove('open');
        document.body.style.overflow = '';
      });
    }

    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) {
        lightbox.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  }

  // 4. Careers: Apply Modal
  const applyButtons = document.querySelectorAll('.btn-apply-job');
  const applyModal = document.getElementById('applyModal');
  const applyModalClose = document.getElementById('applyModalClose');
  const applyJobIdInput = document.getElementById('applyJobId');
  const applyJobTitleDisplay = document.getElementById('applyJobTitleDisplay');

  if (applyButtons.length > 0 && applyModal) {
    applyButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const jobId = btn.getAttribute('data-job-id');
        const jobTitle = btn.getAttribute('data-job-title');

        if (applyJobIdInput) applyJobIdInput.value = jobId;
        if (applyJobTitleDisplay) applyJobTitleDisplay.textContent = `Applying for: ${jobTitle}`;

        applyModal.classList.add('open');
        document.body.style.overflow = 'hidden';
      });
    });

    if (applyModalClose) {
      applyModalClose.addEventListener('click', () => {
        applyModal.classList.remove('open');
        document.body.style.overflow = '';
      });
    }

    applyModal.addEventListener('click', (e) => {
      if (e.target === applyModal) {
        applyModal.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  }

  // 5. Global Escape key handling for Modals
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (lightbox && lightbox.classList.contains('open')) {
        lightbox.classList.remove('open');
        document.body.style.overflow = '';
      }
      if (applyModal && applyModal.classList.contains('open')) {
        applyModal.classList.remove('open');
        document.body.style.overflow = '';
      }
      if (drawer && drawer.classList.contains('open')) {
        closeDrawer();
      }
    }
  });

  // 6. Three.js Hero Scene (for home page if canvas is present and Three.js loaded)
  const canvas = document.getElementById('heroCanvas');
  if (canvas && typeof THREE !== 'undefined') {
    (function initHeroThree() {
      const section = canvas.closest('.home-hero');
      if (!section) return;

      let width = section.clientWidth;
      let height = section.clientHeight;

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
      camera.position.set(0, 0, 14);

      let renderer;
      try {
        renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.setSize(width, height);
      } catch (e) {
        return;
      }

      // Colors
      const colGold = new THREE.Color(0xddb35c);
      const colSage = new THREE.Color(0x9fae86);
      const colTeal = new THREE.Color(0x2c6a63);
      const colBlush = new THREE.Color(0xefc3ac);
      const palette = [colGold, colSage, colTeal, colBlush];

      // Particles
      const count = window.innerWidth < 768 ? 90 : 180;
      const positions = new Float32Array(count * 3);
      const colors = new Float32Array(count * 3);

      for (let i = 0; i < count; i++) {
        const r = 6 + Math.random() * 7;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(Math.random() * 2 - 1);
        positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
        positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta) * 0.6;
        positions[i * 3 + 2] = r * Math.cos(phi) * 0.6 - 2;

        const c = palette[i % palette.length];
        colors[i * 3] = c.r;
        colors[i * 3 + 1] = c.g;
        colors[i * 3 + 2] = c.b;
      }

      const pGeo = new THREE.BufferGeometry();
      pGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      pGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

      const pMat = new THREE.PointsMaterial({
        size: window.innerWidth < 768 ? 0.08 : 0.11,
        vertexColors: true,
        transparent: true,
        opacity: 0.85
      });
      const points = new THREE.Points(pGeo, pMat);
      scene.add(points);

      // Animation
      let targetX = 0, targetY = 0, curX = 0, curY = 0;
      window.addEventListener('mousemove', (e) => {
        targetX = (e.clientX / window.innerWidth - 0.5) * 2;
        targetY = (e.clientY / window.innerHeight - 0.5) * 2;
      }, { passive: true });

      const clock = new THREE.Clock();
      function animate() {
        requestAnimationFrame(animate);
        const t = clock.getElapsedTime();

        curX += (targetX - curX) * 0.04;
        curY += (targetY - curY) * 0.04;

        camera.position.x = curX * 1.1;
        camera.position.y = -curY * 0.7;
        camera.lookAt(0, 0, 0);

        points.rotation.y = t * 0.025;
        points.rotation.x = Math.sin(t * 0.08) * 0.04;

        renderer.render(scene, camera);
      }
      animate();

      window.addEventListener('resize', () => {
        width = section.clientWidth;
        height = section.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
      });
    })();
  }
});
