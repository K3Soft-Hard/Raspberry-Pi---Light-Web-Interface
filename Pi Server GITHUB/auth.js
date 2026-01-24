// auth.js - Final Version (Shows Background)
async function runAuth() {
    // 1. Wait for the page to load so we can find the elements
    window.addEventListener('DOMContentLoaded', async () => {
        const topBar = document.querySelector('.top-bar');
        const sidePanel = document.querySelector('.side-panel');

        // Hide UI immediately if not unlocked
        if (sessionStorage.getItem('pi_unlocked') !== 'true') {
            if (topBar) topBar.style.display = 'none';
            if (sidePanel) sidePanel.style.display = 'none';
        }

        try {
            const response = await fetch('/auth-config.json');
            const config = await response.json();

            if (config.auth_enabled) {
                let isUnlocked = sessionStorage.getItem('pi_unlocked');

                while (isUnlocked !== 'true') {
                    const entry = prompt("Enter Password:");
                    
                    if (entry === null) {
                        window.location.href = "about:blank";
                        return;
                    }

                    if (entry === config.password) {
                        sessionStorage.setItem('pi_unlocked', 'true');
                        isUnlocked = 'true';
                    } else {
                        alert("Wrong Password!");
                    }
                }
            }
            
            // Show UI once authorized
            if (topBar) topBar.style.display = 'flex';
            if (sidePanel) sidePanel.style.display = 'flex';

        } catch (e) {
            console.error("Auth Error:", e);
        }
    });
}

function logoutPi() {
    if(confirm("Logout and lock the dashboard?")) {
        sessionStorage.removeItem('pi_unlocked');
        window.location.reload(); 
    }
}

runAuth();