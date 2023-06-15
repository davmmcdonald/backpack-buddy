function dismissAlert(button) {
    button.parentNode.remove();
}

function copyUrl() {
    const url = window.location.href;
    navigator.clipboard.writeText(url);
    alert('List URL copied to clipboard!');
}

// function refreshImage(imageSelector) {
//     imageSelector.nextElementSibling.src = `static/assets/card-images/${imageSelector.value}`;
// }

function initAutocomplete() {
    const locationInput = document.getElementById('location');
    const autocomplete = new google.maps.places.Autocomplete(locationInput);
}
google.maps.event.addDomListener(window, 'load', initAutocomplete);

function deleteList(deleteListButton) {
    listId = deleteListButton.dataset.listId;
    fetch('/delete-list', {
        method: "POST",
        body: JSON.stringify({ listId: listId })
    }).then((_res) => {
        window.location.href = '/dashboard';
    });
}

function deleteGear(deleteGearButton) {
    gearId = deleteGearButton.dataset.gearId;
    listId = deleteGearButton.dataset.listId
    fetch('/delete-gear', {
        method: "POST",
        body: JSON.stringify({ gearId: gearId, listId: listId })
    }).then((_res) => {
        window.location.reload();
    });
}

// const categories = document.querySelectorAll('.category');
// categories.forEach(element => {
//     if (!element.nextElementSibling.classList.contains('card-wrapper')) {
//         const placeholder = document.createElement('div');
//         placeholder.classList.add('gear-placeholder');
//         const placeholderText = document.createElement('p');
//         placeholderText.innerText = 'Add more gear!';
//         placeholderText.classList.add('placeholder-message');
//         placeholder.appendChild(placeholderText);
//         element.after(placeholder);
//     }
// });