<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
// Ничего не нужно, router-view сам управляет компонентами
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #e0e0e0;
}

#app {
  width: 100%;
  min-height: 100vh;
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}
</style>
