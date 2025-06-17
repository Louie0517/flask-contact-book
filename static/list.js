
let menuOpen = false;

function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    const button = document.querySelector('.mobile-menu-btn');

    menuOpen = !menuOpen;

    if(menuOpen) {
        menu.classList.add('active');
        button.style.transform = 'rotate(90deg)';
        button.innerHTML = '✕';
    } else {
        menu.classList.remove('active');
        button.style.transform = 'rotate(0deg)';
        button.innerHTML = '☰';
    }
}


function toggleDarkMode() {
        
    const text = document.getElementById("dark-mode-text")
    const icon = document.getElementById("darkIcon");
    const body = document.body;

    document.body.classList.toggle("dark-mode");

    if(document.body.classList.contains("dark-mode")) {
        icon.classList.replace("fa-cloud-moon", "fa-cloud-sun");
        text.textContent = "Light Mode";
    } else {
        icon.classList.replace("fa-cloud-sun", "fa-cloud-moon");
        text.textContent = "Dark Mode";
    }
}

document.addEventListener('click', function(event) {
    const mobileMenu = document.getElementById('mobileMenu');
    const button = document.querySelector('.mobile-menu-btn');

    if(menuOpen && !mobileMenu.contains(event.target) && !button.contains(event.target)) {
        toggleMobileMenu()
    }
});



document.querySelectorAll('.mobile-menu a').forEach(link => {
            link.addEventListener('click', function(e) {
                if (this.getAttribute('href').startsWith('#')) {
                    e.preventDefault();
                    const action = this.getAttribute('href').substring(1);
                    
                    switch(action) {
                        case 'friends':
                            alert('Friends page clicked!');
                            break;
                        case 'edit':
                            alert('Edit page clicked!');
                            break;
                        case 'logout':
                            if (confirm('Are you sure you want to logout?')) {
                                alert('Logging out...');
                            }
                            break;
                    }
                    
                    if (menuOpen) {
                        toggleMobileMenu();
                    }
                }
            });
        });


function darkMode() {
    const deskIcon = document.getElementById('dark-mode-i');
    const txt = document.getElementById('dark-txt');
    const deskBody = document.body;

    deskBody.classList.toggle('dark-desk');
    if (deskBody.classList.contains('dark-desk')) {
        deskIcon.classList.replace("fa-cloud-moon", "fa-cloud-sun");
        txt.textContent = "Light Mode";
    } else {
        deskIcon.classList.replace("fa-cloud-sun", "fa-cloud-moon");
        txt.textContent = "Dark Mode";
    }


}