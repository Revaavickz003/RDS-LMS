document.addEventListener("DOMContentLoaded", function () {
    var listItems = document.querySelectorAll("#busstype-options ul li");
    var textarea = document.getElementById("busstype-textarea");
    var filterBusstype = document.getElementById("filter-busstype");

    if (!textarea) {
        console.error("Textarea element not found.");
        return;
    }

    listItems.forEach(function (item, index) {
        item.addEventListener("click", function () {
            var selectedValue = item.textContent.trim();

            // Deselect all items
            listItems.forEach(function (otherItem) {
                if (otherItem !== item) {
                    otherItem.classList.remove("selected");
                }
            });

            if (item.classList.contains("selected")) {
                // If the clicked item is already selected, deselect it
                item.classList.remove("selected");
                textarea.value = '';
                filterBusstype.classList.remove("completed");
            } else {
                // Select the clicked item
                item.classList.add("selected");
                textarea.value = selectedValue;
                filterBusstype.classList.add("completed");
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var locationList = document.getElementById("location-list");
    var locationInput = document.getElementById("location-options");
    var addLocationBtn = document.getElementById("add-location-btn");
    var locationTextarea = document.getElementById("location-textarea");

    addLocationBtn.addEventListener("click", function () {
        var locationName = locationInput.value.trim();

        if (locationName !== "") {
            // Remove any previously selected location
            var selectedItems = document.querySelectorAll("#location-list .selected");
            selectedItems.forEach(function (item) {
                locationList.removeChild(item);
            });

            // Add the new location
            var listItem = document.createElement("li");
            listItem.textContent = locationName;
            listItem.classList.add("selected");

            listItem.addEventListener("click", function () {
                listItem.classList.toggle("selected");
                updateTextarea();
            });

            locationList.appendChild(listItem);
            locationInput.value = "";
            updateTextarea();
        }
    });

    function updateTextarea() {
        var selectedLocation = "";
        var selectedItem = document.querySelector("#location-list .selected");

        if (selectedItem) {
            selectedLocation = selectedItem.textContent;
        }

        locationTextarea.value = selectedLocation;
    }
});


document.addEventListener("DOMContentLoaded", function () {
    var budgetList = document.getElementById("budget-list");
    var budgetTextarea = document.getElementById("budget-textarea");

    budgetList.addEventListener("click", function (event) {
        if (event.target.tagName === "LI") {
            // Deselect all items
            var allItems = document.querySelectorAll("#budget-list li");
            allItems.forEach(function (item) {
                item.classList.remove("selected");
            });

            // Select the clicked item
            event.target.classList.add("selected");
            updateTextarea();
        }
    });

    function updateTextarea() {
        var selectedBudget = "";
        var selectedItem = document.querySelector("#budget-list .selected");

        if (selectedItem) {
            selectedBudget = selectedItem.textContent.trim();
        }

        budgetTextarea.value = selectedBudget;
    }
});

document.addEventListener("DOMContentLoaded", function () {
    var fudOptionsList = document.getElementById("fud-options-list");
    var fudDateInput = document.getElementById("fud-date-input");
    var addFudBtn = document.getElementById("add-fud-btn");
    var fudTextarea = document.getElementById("fud-textarea");

    addFudBtn.addEventListener("click", function () {
        var dateValue = fudDateInput.value;

        if (dateValue !== "") {
            // Remove any previously selected date
            var selectedItems = document.querySelectorAll("#fud-options-list .selected");
            selectedItems.forEach(function (item) {
                fudOptionsList.removeChild(item);
            });

            // Add the new date
            var listItem = document.createElement("li");
            listItem.textContent = dateValue;
            listItem.classList.add("selected");

            listItem.addEventListener("click", function () {
                listItem.classList.toggle("selected");
                updateTextarea();
            });

            fudOptionsList.appendChild(listItem);
            fudDateInput.value = "";
            updateTextarea();
        }
    });

    function updateTextarea() {
        var selectedDate = "";
        var selectedItem = document.querySelector("#fud-options-list .selected");

        if (selectedItem) {
            selectedDate = selectedItem.textContent;
        }

        fudTextarea.value = selectedDate;
    }
});



document.addEventListener("DOMContentLoaded", function () {
    // Priority
    var priorityOptionsList = document.getElementById("priority-options-list");
    var priorityTextarea = document.getElementById("priority-textarea");

    priorityOptionsList.addEventListener("click", function (event) {
        handleSingleSelection(event, priorityOptionsList, priorityTextarea);
    });

    // Source
    var sourceOptionsList = document.getElementById("source-options-list");
    var sourceTextarea = document.getElementById("source-textarea");

    sourceOptionsList.addEventListener("click", function (event) {
        handleSingleSelection(event, sourceOptionsList, sourceTextarea);
    });

    // Services
    var servicesOptionsList = document.getElementById("services-options-list");
    var servicesTextarea = document.getElementById("services-textarea");

    servicesOptionsList.addEventListener("click", function (event) {
        handleSingleSelection(event, servicesOptionsList, servicesTextarea);
    });

    // Business Type
    var businessTypeOptionsList = document.getElementById("business-type-options-list");
    var businessTypeTextarea = document.getElementById("business-type-textarea");

    businessTypeOptionsList.addEventListener("click", function (event) {
        handleSingleSelection(event, businessTypeOptionsList, businessTypeTextarea);
    });

    function handleSingleSelection(event, optionsList, textarea) {
        if (event.target.tagName === "LI") {
            // Deselect all items
            var allItems = optionsList.querySelectorAll(".selected");
            allItems.forEach(function (item) {
                item.classList.remove("selected");
            });

            // Select the clicked item
            event.target.classList.add("selected");
            updateTextarea(optionsList, textarea);
        }
    }

    function updateTextarea(optionsList, textarea) {
        var selectedOption = "";
        var selectedItem = optionsList.querySelector(".selected");

        if (selectedItem) {
            selectedOption = selectedItem.textContent;
        }

        textarea.value = selectedOption;
    }
});

