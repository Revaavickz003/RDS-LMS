document.addEventListener("DOMContentLoaded", function () {
    document.querySelector('.task-list').addEventListener('click', function (event) {
        var clickedElement = event.target;
        var optionsContainer = clickedElement.nextElementSibling;

        if (clickedElement.classList.contains('completed') && optionsContainer) {
            hideAllOptionContainers(optionsContainer.id);
            optionsContainer.classList.toggle("show-options");
        }
    });

    function hideAllOptionContainers(excludeOptionsDivId) {
        var allOptionContainers = document.querySelectorAll('.options');
        allOptionContainers.forEach(function (container) {
            if (container.id !== excludeOptionsDivId) {
                container.classList.remove('show-options');
            }
        });
    }


    // Autocomplete functionality for the location options
    $("#location-options").autocomplete({
        source: function (request, response) {
            // Replace this with your actual data source or API call
            var availableLocations = [
        "Out of Chennai","Abhiramapuram", "Adambakkam", "Adyar", "Agaram", "Alandur", "Alapakkam", "Alwarpet", "Alwarthirunagar",
        "Ambattur", "Ambattur Industrial Estate", "Ambattur OT", "Aminjikarai", "Anna Nagar", "Anna Nagar East",
        "Anna Nagar Western Extension", "Anna Nagar West", "Anna Road", "Anna Salai", "Arcot Road", "Arumbakkam",
        "Ashok Nagar", "Attipatttu", "Avadi", "Ayanavaram", "Ayyappanthangal", "Besant Nagar", "Broadway",
        "Cathedral Road", "Chepauk", "Chetpet", "Chinmaya Nagar", "Chintadripet", "Choolai", "Choolaimedu",
        "CIT Nagar", "East Coast Road", "Egmore", "Ekkatuthangal", "Ennore", "Ernavur", "Erukkancheri",
        "Flowers Road", "Gandhi Nagar", "George Town", "Gopalapuram", "Gowrivakkam", "Greams Road", "Guindy",
        "Guindy Industrial Estate", "Gurukkambakkam", "Haddows Road", "Hastinapuram", "IIT Madras", "Indira Nagar",
        "Injambakkam", "Jafferkhanpet", "Jawahar Nagar", "Kaladipet", "Kamaraj Nagar", "Kandanchavadi", "Karambakkam",
        "Karapakkam", "Kattupakkam", "Kellys", "Kilpauk", "Kilpauk Garden", "KK Nagar", "KK Nagar West", "Kodambakkam",
        "Kodungaiyur", "Kolathur", "Kondithope", "Korattur", "Korukkupet", "Kottivakkam", "Kottur", "Kotturpuram",
        "Kovilambakkam", "Koyambedu", "Kosapet", "Little Mount", "Madambakkam", "Madhavaram", "Madipakkam",
        "Maduravoyal", "Mahalingapuram", "Mambalam", "Manali", "Manapakkam", "Mandaveli", "Mandavelipakkam",
        "Mangadu", "Mannady", "Mannurpet", "Medavakkam", "Meenambakkam", "Metha Nagar", "Mettukuppam", "MGR Nagar",
        "MKB Nagar", "Mogapper", "Mogapper East", "Mogapper West", "Moolakadai", "Mount Road", "Mylapore",
        "Nammalwarpt", "Nandambakkam", "Nandanam", "Nandanam extension", "Nanganallur", "Nehru Nagar",
        "Nelson Manickam Road", "Nerkundram", "Nesapakkam", "New Perungalathur", "New Washermanpet", "Neelankarai",
        "North Usman Road", "Nungambakkam", "Nungambakkam High Road", "Old Mahabalipuram Road", "Old Pallavaram",
        "Old Washermanpet", "Otteri", "Padi", "Palavakkam", "Palavanthangal", "Pallavaram", "Pallikaranai", "Pammal",
        "Park Town", "Parrys", "Pattalam", "Pazhavanthangal", "Perambur", "Perambur Barracks Road", "Peravallur",
        "Periyamedu", "Periyar Nagar", "Perungudi", "Polichalur", "Pondy Bazaar", "Ponniammanmedu", "Poonamalle High Road",
        "Porur", "Pozhichalur", "Pudupet", "Pulianthope", "Puludivakkam", "Purasavakkam", "Purasavakkam High Road",
        "RA Puram", "Raja Annamalai Puram", "Rajaji Salai", "Rajakilpakkam", "Ramapuram", "Rangarajapuarm", "Royapettah",
        "Royapettah high road", "Royapuram", "Saidapet", "Saidapet West", "Saligramam", "Santhome", "Selaiyur", "Sembakkam",
        "Seven Wells", "Shastri Nagar", "Shenoy Nagar", "Sholinganallur", "SIDCO Industrial Estate", "Sholinganallur",
        "Sowcarpet", "Spencer Plaza", "Srinivasa Nagar", "St Thomas Mount", "Parangi Malai", "T. Nagar", "Thillai Ganga Nagar",
        "Taramani", "Teynampet", "Tharamani", "Thirumangalam", "Thirmulaivoyal", "Thiruvallikeni", "Thiruvanmiyur",
        "Thiruverkadu", "Tiruvottiyur", "Thuraipakkam", "Thousand Lights", "Thiyagaraya Nagar", "Tirumullaivayal",
        "Tiruvottiyur", "Thuraipakkam", "Thousand Lights", "Thiyagaraya Nagar", "Tirumullaivayal", "Thiruvallikeni",
        "Thiruverkadu Road", "Tondiarpet", "Triplicane", "Triplicane High Road", "Triplicane South", "Ullagaram",
        "Urapakkam", "Valasaravakkam", "Vanagaram", "Velachery", "Velachery Main Road", "Vepery", "Villivakkam",
        "Virugambakkam", "Vyasarpadi", "Washermanpet", "West CIT Nagar", "West K.K. Nagar", "West Mambalam", "Mogappair West",
        "West Saidapet"
            ];
            var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(request.term), "i");
            response($.grep(availableLocations, function (item) {
                return matcher.test(item);
            }));
        },
        minLength: 0,
        messages: {
            noResults: '',
            results: function () {}
        }
    });
});


