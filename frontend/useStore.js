import create from 'zustand';

export const useStore = create((set) => ({
  recipes: [],
  fetchRecipes: async (ingredients) => {
    const response = await fetch(`/api/search?ingredients=${ingredients}`);
    const data = await response.json();
    set({ recipes: data });
  },
  // other store methods...
}));
