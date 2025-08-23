import React, { useState } from 'react';

const IngredientInput = ({ onSearch }) => {
  const [ingredients, setIngredients] = useState('');

  const handleSearch = () => {
    onSearch(ingredients);
  };

  return (
    <div>
      <input
        type="text"
        value={ingredients}
        onChange={(e) => setIngredients(e.target.value)}
        placeholder="Enter ingredients..."
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
};

export default IngredientInput;
