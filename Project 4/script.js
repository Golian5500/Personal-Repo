document.addEventListener('DOMContentLoaded', function () {
    const titleofpage = document.querySelector('.webpage_title');
    const expandMoreOption = document.getElementById('expand_more_option');
    const dropdownContainer = document.querySelector('.dropdown-container');
    const expandImg = expandMoreOption.querySelector('img');
    const expandText = expandMoreOption.querySelector('p');
    const expandAddLabel = document.querySelector('.label-add');
    const addLabelUI = document.querySelector('.create-new-label-container');
    const grayBackground = document.querySelector('.graying-background');
    const cancelCreatingALabel = document.querySelector('.cancel-add-new-label');

    function updateActiveState() {
        let currentHash = window.location.hash;

        if (currentHash === "" || currentHash === "#") {
            history.replaceState(null, '', '#inbox');
            currentHash = "#inbox";
        }

        const activeHash = currentHash.substring(1);

        const allMenuItems = document.querySelectorAll('.option:not(#expand_more_option)');

        allMenuItems.forEach(element => {
            element.classList.remove('active-rn');
            const img = element.querySelector('img');
            if (img) {
                const name = element.classList[0].split('-')[0];
                img.src = `images/${name}_empty.png`;
            }
        });

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

            if (dropdownContainer && dropdownContainer.contains(newActiveElement)) {
                openDropdown();
            }
        }
    }

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
        isExpanded ? closeDropdown() : openDropdown();
    });

    expandAddLabel.addEventListener('click', function (e) {
        e.preventDefault();
        addLabelUI.style.display = 'block'
        grayBackground.style.display = 'block'
    });

    cancelCreatingALabel.addEventListener('click', function (e) {
        e.preventDefault();
        addLabelUI.style.display = 'none'
        grayBackground.style.display = 'none'
    });

    grayBackground.addEventListener('click', function (e) {
        e.preventDefault();
        addLabelUI.style.display = 'none'
        grayBackground.style.display = 'none'
    });

    updateActiveState();
    window.addEventListener('hashchange', updateActiveState);
});