document.addEventListener('DOMContentLoaded', function () {
    const titleofpage = document.querySelector('.webpage_title');
    const expandMoreOption = document.getElementById('expand_more_option');
    const dropdownContainer = document.querySelector('.dropdown-container');
    const expandImg = expandMoreOption.querySelector('img');
    const expandText = expandMoreOption.querySelector('p');

    function updateActiveState() {
        let currentHash = window.location.hash;

        // 1. Default Hash
        if (currentHash === "" || currentHash === "#") {
            history.replaceState(null, '', '#inbox');
            currentHash = "#inbox";
        }

        const activeHash = currentHash.substring(1);
        
        // 2. Select ALL options (including the ones in dropdown)
        // We exclude the 'expand_more_option' itself from being highlighted as a page
        const allMenuItems = document.querySelectorAll('.option:not(#expand_more_option)');

        allMenuItems.forEach(element => {
            element.classList.remove('active-rn');
            const img = element.querySelector('img');
            if (img) {
                // This logic takes "inbox-option" and gets "inbox"
                const name = element.classList[0].split('-')[0];
                img.src = `images/${name}_empty.png`;
            }
        });

        // 3. Set New Active State
        const newActiveElement = document.querySelector(`.${activeHash}-option`);

        if (newActiveElement) {
            newActiveElement.classList.add("active-rn");

            const activeImg = newActiveElement.querySelector('img');
            if (activeImg) {
                activeImg.src = `images/${activeHash}.png`;
            }

            if (titleofpage) {
                titleofpage.textContent = activeHash.charAt(0).toUpperCase() + activeHash.slice(1) + " - hajzerajdrin@gmail.com - Gmail";
            }

            // AUTO-EXPAND: If the active item is inside the dropdown, open it
            if (dropdownContainer && dropdownContainer.contains(newActiveElement)) {
                openDropdown();
            }
        }
    }

    // --- Dropdown Logic ---
    let isExpanded = false;

    function openDropdown() {
        isExpanded = true;
        dropdownContainer.style.display = 'block'; 
        expandImg.src = 'images/expand.png';
        expandText.innerHTML = 'Less';
    }

    function closeDropdown() {
        isExpanded = false;
        dropdownContainer.style.display = 'none';
        expandImg.src = 'images/expand_empty.png';
        expandText.innerHTML = 'More';
    }

    expandMoreOption.addEventListener('click', function (e) {
        e.preventDefault();
        // If we are clicking 'Less' and the active page is inside the dropdown,
        // you might want to keep it open, but usually, Gmail allows closing it.
        isExpanded ? closeDropdown() : openDropdown();
    });

    // --- Initialize ---
    updateActiveState();
    window.addEventListener('hashchange', updateActiveState);
});