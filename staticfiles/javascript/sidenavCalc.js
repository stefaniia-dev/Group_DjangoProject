
window.addEventListener('load', adjustHeight);
window.addEventListener('resize', adjustHeight);

function adjustHeight() {
  const sideNav = document.querySelector('.sideNav');
  const mainContent = document.querySelector('.main_content');

  if (sideNav && mainContent) {
    const contentHeight = mainContent.scrollHeight; // Gets the full height of the content

    sideNav.style.height = `${Math.max(contentHeight, window.innerHeight)}px`;
  }
}

/* OLLLD ATTEMPT
window.addEventListener('load', adjustHeight);
window.addEventListener('resize', adjustHeight);


function adjustHeight() {
  const sideNav = document.querySelector('.sideNav');
  const mainContent = document.querySelector('.main_content');

  const contentHeight = mainContent.scrollHeight;

  sideNav.style.height = `${Math.max(contentHeight, window.innerHeight)}px`;
}
 */