
var categoryElement = document.getElementById('category');
var subcategoryElement = document.getElementById('subcategory');

if (categoryElement) {

    function disableElements() {
        categoryElement.disabled = true;
        subcategoryElement.disabled = true;
    }

    function enableElements() {
        categoryElement.disabled = false;
        subcategoryElement.disabled = false;
    }

    function setSubcategories(options) {
        subcategoryElement.innerHTML = '';

        for(let i = 0; i < options.length; ++i) {
            let option = options[i];
            let optionElement = document.createElement('option');
            optionElement.value = option[0];
            optionElement.innerText = option[1];
            subcategoryElement.append(optionElement);
        }

        enableElements();
    }

    function onChangeCategory(category) {
        categoryElement.disabled = true;
        subcategoryElement.disabled = true;
        fetch('/api/categories/' + category)
            .then(response => {
                if (!response.ok) {
                    resetElements();
                    throw new Error('Bad Response');
                }
                return response.json();
            }).then(jsonData => setSubcategories(jsonData));
    }

    categoryElement.addEventListener('change', event => {
        onChangeCategory(event.target.value);
    })
}