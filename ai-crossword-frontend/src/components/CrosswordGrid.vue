<template>
  <div v-if="grid && grid.length" class="inline-block border border-gray-400">
    <table class="border-collapse">
      <thead>
      <tr>
        <th class="w-8 h-8"></th>
        <th
          v-for="(_, c) in grid[0]"
          :key="'col-' + c"
          class="w-8 h-8 text-center border border-gray-400 bg-gray-100 font-mono"
        >
          {{ c + 1 }}
        </th>
      </tr>
      </thead>
      <tbody>
       <tr v-for="(row, r) in grid" :key="r">
          <!-- Row number -->
          <th
            class="w-8 h-8 text-center border border-gray-400 bg-gray-100 font-mono"
          >
            {{ r + 1 }}
          </th>

          <!-- Actual crossword cells -->

          <td
            v-for="(cell, c) in row"
            :key="c"
            class="w-8 h-8 text-center border border-gray-400 font-mono"
            :class="cell.value ? 'bg-yellow-50' : 'bg-gray-200'"
          >
            {{ cell.value ? (cell.status == 'hidden' ? "?" : cell.value) : '' }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <p v-else class="text-gray-500">No crossword generated yet.</p>
</template>

<script setup>
defineProps({
  grid: Array
});
</script>

