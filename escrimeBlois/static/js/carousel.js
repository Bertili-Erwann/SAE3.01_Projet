document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.carousel-row').forEach(function (row) {
    const container = row.querySelector('.articles');
    const prev = row.querySelector('.carousel-btn.prev');
    const next = row.querySelector('.carousel-btn.next');
    if (!container || !prev || !next) return;

    const step = () => Math.max(container.clientWidth * 0.8, 200);
    prev.addEventListener('click', () => container.scrollBy({ left: -step(), behavior: 'smooth' }));
    next.addEventListener('click', () => container.scrollBy({ left:  step(), behavior: 'smooth' }));
  });
});
