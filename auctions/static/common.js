document.addEventListener('DOMContentLoaded', function () {
    const navbarContainer = document.getElementById('navbar');

    if (navbarContainer) {
        navbarContainer.innerHTML = `
            <div class="navbar">
                <div class="logo">
                    <img src="your-logo-url-here.png" alt="Logo">
                    <h1>Auction Site</h1>
                </div>
            </div>
        `;
    }
});
