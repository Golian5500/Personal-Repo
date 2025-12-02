document.addEventListener('DOMContentLoaded', function() {
  function updateActiveState() {
    const currentHash = window.location.hash;
    
    if (currentHash === "" || currentHash === "#") {
      history.replaceState(null, '', '#inbox');
    }

    const activeHash = window.location.hash.substring(1);
    const allMenuItems = document.querySelectorAll('.inbox-option, .starred-option, .snoozed-option, .sent-option, .drafts-option, .purchase-option');

    allMenuItems.forEach(element => {
      element.classList.remove('active-rn');
    });

    let newActiveElement;

    switch (activeHash) {
      case 'inbox':
        newActiveElement = document.querySelector(".inbox-option");
        break;
      case 'starred':
        newActiveElement = document.querySelector(".starred-option");
        break;
      case 'snoozed':
        newActiveElement = document.querySelector(".snoozed-option");
        break;
      case 'sent':
        newActiveElement = document.querySelector(".sent-option");
        break;
      case 'drafts':
        newActiveElement = document.querySelector(".drafts-option");
        break;
      case 'purchase':
        newActiveElement = document.querySelector(".purchase-option");
        break;
    }

    if (newActiveElement) {
      newActiveElement.classList.add("active-rn");
    }
  }

  updateActiveState();

  window.addEventListener('hashchange', updateActiveState);
});