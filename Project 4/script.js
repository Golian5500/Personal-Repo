document.addEventListener('DOMContentLoaded', function() {
  function updateActiveState() {
    const currentHash = window.location.hash;
    // Note: ensure your HTML has class="webpage_title" or change to match your ID
    const titleofpage = document.querySelector('.webpage_title');
    
    // Default to #inbox if no hash exists
    if (currentHash === "" || currentHash === "#") {
      history.replaceState(null, '', '#inbox');
    }

    const activeHash = window.location.hash.substring(1);
    const allMenuItems = document.querySelectorAll('.inbox-option, .starred-option, .snoozed-option, .sent-option, .drafts-option, .purchase-option');

    allMenuItems.forEach(element => {
      element.classList.remove('active-rn');

      const img = element.querySelector('img');
      if (img) {
        // Extracts "inbox" from "inbox-option"
        const name = element.classList[0].split('-')[0]; 
        img.src = `images/${name}_empty.png`;
      }
    });

    const newActiveElement = document.querySelector(`.${activeHash}-option`);

    if (newActiveElement) {
      newActiveElement.classList.add("active-rn");
      
      // 1. Update the Image
      const activeImg = newActiveElement.querySelector('img');
      if (activeImg) {
        activeImg.src = `images/${activeHash}.png`;
      }

      // 2. Update the Page Title
      if (titleofpage) {
        // Capitalizes the first letter (e.g., "inbox" -> "Inbox")
        titleofpage.textContent = activeHash.charAt(0).toUpperCase() + activeHash.slice(1) + " - hajzerajdrin@gmail.com";
      }
    }
  }

  updateActiveState();
  window.addEventListener('hashchange', updateActiveState);
});