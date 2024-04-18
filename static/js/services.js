const addServiceBtn = document.getElementById('add-service-btn');
    const servicesList = document.getElementById('services-list');
    const moreInput = document.getElementById('more-input');
    const selectedServicesInput = document.getElementById('selected-services-input');
    const selectedServices = [];

    // Initialize selected services based on existing services
    servicesList.querySelectorAll('li.selected').forEach((serviceItem) => {
      const serviceName = serviceItem.textContent.trim();
      selectedServices.push(serviceName);
    });

    function updateSelectedServices() {
      selectedServicesInput.value = JSON.stringify(selectedServices);
      console.log('Selected Services:', selectedServices);
    }

    addServiceBtn.addEventListener('click', () => {
      const serviceName = moreInput.value.trim();
      if (serviceName !== '') {
        const newServiceItem = document.createElement('li');
        newServiceItem.textContent = serviceName;
        newServiceItem.classList.add('selected');

        // Find the index of "Yet to Confirm"
        const yetToConfirmIndex = Array.from(servicesList.children).findIndex(item => item.textContent.trim() === 'Yet to Confirm');

        // Insert the new service after "Yet to Confirm"
        servicesList.insertBefore(newServiceItem, servicesList.children[yetToConfirmIndex + 1]);

        moreInput.value = '';

        selectedServices.push(serviceName);
        updateSelectedServices();
      }
    });

    servicesList.addEventListener("click", function (e) {
      const target = e.target;

      if (target.tagName === "LI" && target.textContent.trim() !== 'More') {
        if (target.classList.contains("selected")) {
          // Deselect the clicked list item
          target.classList.remove("selected");
          const serviceName = target.textContent.trim();
          const index = selectedServices.indexOf(serviceName);
          if (index !== -1) {
            selectedServices.splice(index, 1);
            updateSelectedServices();
          }
        } else {
          // Select the clicked list item
          target.classList.add('selected');
          const serviceName = target.textContent.trim();
          selectedServices.push(serviceName);
          updateSelectedServices();
        }
      }
    });

    const moreBtn = document.getElementById('more-btn');
    const inputContainer = document.getElementById('input-container-id');

    moreBtn.addEventListener('click', () => {
      inputContainer.classList.toggle('show-input-container');
    });