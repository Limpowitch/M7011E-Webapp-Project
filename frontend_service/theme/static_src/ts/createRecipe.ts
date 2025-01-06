document.addEventListener('DOMContentLoaded', () => {
    // Store units options from the initial ingredient select element
    const initialSelect = document.querySelector('#ingredients-list select') as HTMLSelectElement | null;
    let unitsOptions = '';

    if (initialSelect) {
        unitsOptions = initialSelect.innerHTML;
    } else {
        console.error('No initial select element found in #ingredients-list.');
        return; // Exit if no initial select element is found
    }
    
    const addInstruction = (): void => {
        const instructionsList = document.getElementById('instructions-list')!;
        const stepNumber = instructionsList.children.length + 1;

        const instructionItem = document.createElement('div');
        instructionItem.className = 'instruction-item';

        instructionItem.innerHTML = `
            <input type="text" name="instructions[]" placeholder="Step ${stepNumber}" required>
            <button type="button" class="remove-instruction">Remove</button>
        `;

        instructionsList.appendChild(instructionItem);
    };

    // Function to add a new ingredient
    const addIngredient = (): void => {
        const ingredientsList = document.getElementById('ingredients-list')!;

        const ingredientItem = document.createElement('div');
        ingredientItem.className = 'ingredient-item';

        ingredientItem.innerHTML = `
            <input type="text" name="ingredients_name[]" placeholder="Ingredient Name" required>
            <input type="number" name="ingredients_amount[]" placeholder="Amount" step="any" required>
            <select name="ingredients_unit[]" required>
                ${unitsOptions}
            </select>
            <button type="button" class="remove-ingredient">Remove</button>
        `;

        ingredientsList.appendChild(ingredientItem);
    };

    // Event listener for adding instructions
    document.getElementById('add-instruction')!.addEventListener('click', addInstruction);

    // Event listener for adding ingredients
    document.getElementById('add-ingredient')!.addEventListener('click', addIngredient);

    // Event delegation for removing instructions and ingredients
    document.addEventListener('click', (event: Event) => {
        const target = event.target as HTMLElement;
        if (target.classList.contains('remove-instruction')) {
            target.parentElement?.remove();
            updateInstructionPlaceholders();
        } else if (target.classList.contains('remove-ingredient')) {
            target.parentElement?.remove();
        }
    });

    // Function to update instruction placeholders
    const updateInstructionPlaceholders = (): void => {
        const instructions = document.querySelectorAll<HTMLInputElement>('#instructions-list .instruction-item input');
        instructions.forEach((input, index) => {
            input.placeholder = `Step ${index + 1}`;
        });
    };
});