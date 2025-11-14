<template>
  <div class="p-4 bg-white rounded-xl shadow-md mb-4">
    <h2 class="text-lg font-semibold mb-2">Create a Crossword in Dutch</h2>
    <div class="mb-2">
      <label class="block text-sm font-medium">Give me a theme</label>
      <input
        v-model="theme"
        placeholder="e.g., Summer, vacations, Christmas"
        class="w-full border p-2 rounded"
      />
    </div>
    <button
      @click="generate"
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      :disabled="loading"
    >
      {{ loading ? "Generating..." : "Generate Crossword" }}
    </button>
  </div>
</template>

<script setup>
import { ref, defineEmits } from "vue";
import { generateCrossword } from "../api";

const wordsInput = ref("");
const theme = ref("");
const loading = ref(false);

const emit = defineEmits(["generated"]);

async function generate() {
  loading.value = true;
  try {
    const words = wordsInput.value
      .split(",")
      .map(w => w.trim())
      .filter(w => w);
    const result = await generateCrossword(words, theme.value);
    emit("generated", result);
  } catch (err) {
    console.log(err)
    alert("Failed to generate crossword. See console for details.");
  } finally {
    loading.value = false;
  }
}
</script>
