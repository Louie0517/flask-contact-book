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

hideSideBar()

updateInput()
