<!-- src/components/NavBar.vue -->
<template>
  <nav class="bg-primary p-4">
    <div class="container mx-auto flex justify-between items-center">
      <!-- Logo and Title -->
      <div class="flex items-center">
        <img :src="logo" alt="Logo" class="h-12 w-12 mr-2" />
        <div class="text-white font-bold text-xl">Perfumedia</div>
      </div>

      <!-- Centered Navigation Links -->
      <ul class="flex space-x-4 justify-center flex-grow">
        <li><router-link to="/" class="text-white hover:text-secondary">Home Page</router-link></li>
        <li><router-link to="/clusters" class="text-white hover:text-secondary">Clusters</router-link></li>
        <li><router-link to="/eda" class="text-white hover:text-secondary">EDA</router-link></li>
        <li><router-link to="/classification" class="text-white hover:text-secondary">Classification</router-link></li>
        <li><router-link to="/about" class="text-white hover:text-secondary">About</router-link></li>
      </ul>

      <!-- Right-Aligned GitHub Link -->
      <div>
        <a
          href="https://github.com/JoanMVPopov/parfumedia"
          target="_blank"
          class="text-white hover:text-secondary flex items-center"
        >
          <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 24 24">
            <path
              fill-rule="evenodd"
              d="M12 2C6.477 2 2 6.484 2 12.005c0 4.419 2.865 8.166 6.839 9.49.5.092.683-.217.683-.483 0-.238-.008-.868-.013-1.703-2.782.605-3.369-1.341-3.369-1.341-.455-1.156-1.11-1.465-1.11-1.465-.908-.62.068-.607.068-.607 1.004.07 1.532 1.032 1.532 1.032.892 1.53 2.34 1.088 2.91.832.09-.647.35-1.088.637-1.339-2.22-.252-4.555-1.113-4.555-4.953 0-1.094.39-1.988 1.03-2.686-.103-.253-.446-1.27.097-2.647 0 0 .84-.27 2.75 1.026a9.579 9.579 0 0 1 2.502-.337c.85.004 1.705.114 2.502.337 1.91-1.296 2.75-1.026 2.75-1.026.544 1.377.2 2.394.098 2.647.64.698 1.03 1.592 1.03 2.686 0 3.849-2.338 4.697-4.566 4.944.36.31.68.92.68 1.854 0 1.338-.012 2.42-.012 2.748 0 .268.18.579.688.481C19.135 20.167 22 16.42 22 12.005 22 6.484 17.523 2 12 2z"
              clip-rule="evenodd"
            />
          </svg>
          GitHub
        </a>
      </div>
    </div>
  </nav>
</template>

<script>
import { defineComponent } from 'vue';
import logoImage from '@/assets/perfume.png';

export default defineComponent({
  name: 'NavBar',
  data() {
    return {
      logo: logoImage,
    };
  },
});
</script>