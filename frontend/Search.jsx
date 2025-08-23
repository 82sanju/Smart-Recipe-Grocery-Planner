import React from 'react';
import IngredientInput from '../components/IngredientInput';
import RecipeList from '../components/RecipeList';
import { useStore } from '../store/useStore';

const Search = () => {
  const { fetchRecipes, recipes } = useStore();

  return (
    <div>
      <h1>Search Recipes</h1>
      <IngredientInput onSearch={fetchRecipes} />
      <RecipeList recipes={recipes} />
    </div>
  );
};

export default Search;
