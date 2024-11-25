document.addEventListener('DOMContentLoaded', () => {
    const decreaseButton = document.getElementById('decreasePortion');
    const increaseButton = document.getElementById('increasePortion'); // Corrected ID
    const portionDisplay = document.getElementById('portionCount');
    const ingredients = document.querySelectorAll('.ingredient-amount');

    if (!decreaseButton || !increaseButton || !portionDisplay || !ingredients) {
        console.error('Portion scaler elements not found.');
        return;
    }

    const basePortionCount: number = parseInt(portionDisplay.textContent || '1');

    let portionCount: number = parseInt(portionDisplay.textContent || '1');

    const updatePortionDisplay = () => {
        portionDisplay.textContent = portionCount.toString();
    };

    const scaleIngredients = () => {
        ingredients.forEach((ingredient) =>{
            const baseAmount = parseFloat(ingredient.getAttribute('data-base-amount') || '1');
            const scaledAmount = (portionCount/basePortionCount) * baseAmount;
            const unitMatch = ingredient.textContent?.match(/[a-zA-Z]+$/);
            const unit = unitMatch ? unitMatch[0] : '';
            const formattedAmount = Number(scaledAmount.toFixed(2));
            ingredient.textContent = `${formattedAmount}${unit}`;

        });
    }

    const decreasePortion = () => {
        if (portionCount > 1) {
            if(basePortionCount == 1){
                portionCount--;
            } else if (portionCount != 2){
                portionCount = portionCount - 2;
            }
            updatePortionDisplay();
            scaleIngredients();
        }
    };

    const increasePortion = () => {
        if(basePortionCount == 1){
            portionCount++;
        } else if (portionCount != basePortionCount*4){
            portionCount = portionCount + 2;
        }
        updatePortionDisplay();
        scaleIngredients();
    };

    decreaseButton.addEventListener('click', decreasePortion);
    increaseButton.addEventListener('click', increasePortion);
});