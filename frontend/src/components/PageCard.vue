<!-- src/components/PageCard.vue -->
<template>
  <div class="w-full sm:w-1/2 md:w-1/4 px-2 mb-4">
    <div
      class="bg-light rounded-lg shadow-md p-6 transition-all duration-300 hover:bg-[#FADFA1] hover:bg-opacity-50 hover:shadow-lg"
    >
      <h2 class="text-xl font-semibold mb-2 underline-animation">
        {{ title }}
      </h2>
      <p class="mb-4">{{ description }}</p>
      <router-link
        :to="route"
        class="text-primary hover:text-accent font-bold"
      >
        Learn More
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageCard',
  props: {
    title: String,
    description: String,
    route: String,
  },
};
</script>

<style scoped>
.underline-animation {
  position: relative;
  display: inline-block; /* Important: Ensure underline only spans text width */
}

.underline-animation::after {
  content: '';
  position: absolute;
  width: 100%; /* Ensures the underline spans the text width */
  //height: 3px; /* Thickness of the underline */
  left: 0;
  bottom: 0;
  background-color: #C96868; /* Primary color */
  transform: scaleX(0); /* Initial state: not visible */
  transform-origin: left;
  transition: transform 0.4s ease-in-out; /* Smooth animation */
}

.underline-animation:hover::after {
  transform: scaleX(1); /* Full width of the text */
  height: 1px;
}
</style>