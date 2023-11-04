document.addEventListener('DOMContentLoaded', function() {
// Получить ссылки на элементы select и кнопку
    const replaceLink = document.getElementById("add_new_category_link");
    const clearCatsBtn = document.getElementById("clear_cat");
    const select_main = document.querySelector(".selectpicker");
    let selectElement = document.querySelector(".dropdown");
    let linkClicked = false;
    let inputElement;

    let optionElements = select_main.options;
    let optionValues = [];

    // Переберите элементы <option> и получите их значения
    for (let i = 0; i < optionElements.length; i++) {
        const value = optionElements[i].value;
        if (value.trim() !== '') {
            optionValues.push(value);
        }
    }
    // console.log(optionValues)


    clearCatsBtn.addEventListener("click", function (event){

        selectElement = document.querySelector(".dropdown");

        let listValuesToRemove = []


        fetch(`/ajax_del_category/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ cat_list: optionValues }),
        })
        .then(response => response.json())
        .then(data => {
            listValuesToRemove = data.cat_list
            // console.log("listValuesToRemove" + " " + listValuesToRemove)

            for (let i = 0; i < listValuesToRemove.length; i++) {
                const optionToRemove = select_main.querySelector(`option[value="${listValuesToRemove[i]}"]`);
                if (optionToRemove) {
                    optionToRemove.remove();
                    optionValues = optionValues.filter(item => !listValuesToRemove.includes(item));
                }

            }
            // console.log(optionValues)
            $('.category-select').selectpicker('refresh');
            $('.selectpicker').selectpicker('render');
        })
        .catch(error => console.error(error));

        this.blur();
    });

    // Добавить обработчик события для ссылки
    replaceLink.addEventListener("click", function (event) {
        event.preventDefault(); // Отменяет стандартное действие ссылки

        linkClicked = !linkClicked;
        if (linkClicked) {
            // Создать новый элемент input
            replaceLink.querySelector("span").textContent = "✕";
            clearCatsBtn.style.display = "none";

            inputElement = document.createElement("input");
            inputElement.type = "text"; // Можете использовать другие типы, например, "number"
            inputElement.id = "id_category";

            selectElement = document.querySelector(".dropdown");

            // Заменить select на input
            selectElement.parentNode.replaceChild(inputElement, selectElement);
            inputElement.focus();


            inputElement.addEventListener('change', function(event){

                if (this.value) {

                    fetch(`/ajax_create_category/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrf_token,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ name: this.value }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        const catId = data.id;
                        const catName = data.name;

                        // Создаем новый option элемент
                        const newOption = document.createElement("option");
                        // Устанавливаем текст и значение для нового option
                        newOption.text = catName;
                        newOption.value = catId;

                        const mySelect = selectElement.querySelector("select");

                        const optionToRemove = mySelect.querySelector(`option[value="${catId}"]`);
                        if (optionToRemove) {
                            optionToRemove.remove();
                        }

                        mySelect.appendChild(newOption);
                        inputElement.parentNode.replaceChild(selectElement, inputElement)
                        optionValues.push(newOption.value);

                        $('.category-select').selectpicker('refresh');
                        newOption.selected = true;
                        $('.selectpicker').selectpicker('render');
                    })
                    .catch(error => console.error(error));


                }
                else {
                    inputElement.parentNode.replaceChild(selectElement, inputElement);
                    $('.selectpicker').selectpicker('render');
                }

                linkClicked = !linkClicked
                replaceLink.querySelector("span").textContent = "+";
                clearCatsBtn.style.display = "inline-block";


            });
        }
        else {
            inputElement.blur();
            replaceLink.querySelector("span").textContent = "+";
            clearCatsBtn.style.display = "inline-block";
            inputElement.parentNode.replaceChild(selectElement, inputElement);
            $('.selectpicker').selectpicker('render');
        }

    });
});