import React from 'react';

const RecipeCard = ({ title, image, onSelect }) => (
  <div>
    <img src={image} alt={title} />
    <h3>{title}</h3>
    <button onClick={onSelect}>Select</button>
  </div>
);

export default RecipeCard;
