function updateInput(){
    const sel = document.getElementById('inputGroupSelect02');
    const inp = document.getElementById('text');

    inp.value = sel.value
}

function qSearch(){
    document.getElementById('search').addEventListener('click', function(){
        
    });
}

function hideSideBar(){
    window.addEventListener('resize', function () {
    const offcanvas = document.getElementById('sidebarOffcanvas');
    const bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvas);

    if (window.innerWidth >= 801 && bsOffcanvas) {
      bsOffcanvas.hide();

    const backdrop = document.querySelector('.offcanvas-backdrop');
    if (backdrop) backdrop.remove();
    }
  });
}

function controlSidebar(){
  document.addEventListener("DOMContentLoaded", () => {
  const submenu = document.getElementById("requestsSubMenu");

  // Temporarily disable transition
  submenu.classList.add("notransition");

  // Get Bootstrap instance (don't toggle it yet)
  const collapseInstance = bootstrap.Collapse.getOrCreateInstance(submenu, {
    toggle: false,
  });

  // Check state from localStorage
  const isOpen = localStorage.getItem("requestsSubMenuOpen") === "true";

  // Immediately apply the correct state (show/hide) without animation
  if (isOpen) {
    submenu.classList.add("show");
    submenu.style.visibility = 'visible';

  } else {
    submenu.classList.remove("show");
    submenu.style.visibility = 'visible';

  }

  // After two animation frames, re-enable transition smoothly
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      submenu.classList.remove("notransition");
    });
  });

  // Track open/close state in localStorage on user action
  submenu.addEventListener("shown.bs.collapse", () => {
    localStorage.setItem("requestsSubMenuOpen", "true");
  });

  submenu.addEventListener("hidden.bs.collapse", () => {
    localStorage.setItem("requestsSubMenuOpen", "false");
  });
});


}
controlSidebar();
hideSideBar()
updateInput()
