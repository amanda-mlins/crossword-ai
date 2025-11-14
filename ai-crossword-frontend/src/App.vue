<template>
  <div class="p-6 bg-gray-50 min-h-screen text-gray-800">
    <h1 class="text-2xl font-bold mb-4 text-center">
      🧩 AI Crossword Puzzle Maker
    </h1>
    <WordInput @generated="handleResult" />
    <div class="flex justify-center mt-6">
      <CrosswordGrid v-if="grid" :grid="grid" />
    </div>
    <div class="flex justify-center mt-6">
      <ClueGrid v-if="clues" :clues="clues" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import WordInput from "./components/WordInput.vue";
import CrosswordGrid from "./components/CrosswordGrid.vue";
import ClueGrid from "./components/ClueGrid.vue";

const grid = ref(null);
const clues = ref(null);

function gridState(item, index) {
  console.log(item + "," + index)
  const elem = { value: item, discovered: false }
}

function handleResult(result) {

  const original = result.grid.map(row =>
                                row.map(str => ({
                                  value: str,
                                  status: str === "" ? "empty" : "show"
                                })))

  grid.value = original
  clues.value = result.clues
  console.log(result.placed_words)
  console.log(result.clues)
  console.log(grid.value)
}
</script>
