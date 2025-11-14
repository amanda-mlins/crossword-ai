<template>
  <div v-if="clues" class="inline-block border border-gray-400">
    <table class="border-collapse">
      <tbody>
        <tr v-for="(item, key) in clues">
            <td> {{ item.position}} -> ({{ item.start + 1 }}, {{ item.end + 1}})</td>
            <td> {{ item.clue }} </td>
        </tr>
      </tbody>
    </table>
  </div>
  <p v-else class="text-gray-500">No clues available</p>
</template>

<script setup>
defineProps({
  clues: Object
});
</script>

