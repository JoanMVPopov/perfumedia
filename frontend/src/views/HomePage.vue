<!-- src/views/HomePage.vue -->
<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-4">Welcome to Perfumedia</h1>
    <p class="mb-8">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ultricies interdum libero, a rhoncus justo porta vitae. Aliquam faucibus id diam non aliquam. Nulla eros est, faucibus non nisl nec, pellentesque euismod purus. In id metus at enim ornare efficitur sed non dolor. Duis consequat viverra faucibus. Aenean tempor elit ac laoreet viverra. Quisque vehicula convallis magna vitae consequat. Cras sollicitudin ac velit ultricies imperdiet.
    </p>
    <div class="flex flex-wrap -mx-2">
      <PageCard
        v-for="(card, index) in cards"
        :key="index"
        :title="card.title"
        :description="card.description"
        :route="card.route"
      />
    </div>
  </div>
</template>

<script>
import PageCard from '../components/PageCard.vue';

export default {
  name: 'HomePage',
  components: {
    PageCard,
  },
  data() {
    return {
      cards: [
        {
          title: 'ETL',
          description: 'See how data is Extracted, Transformed and Loaded',
          route: '/etl',
        },
        {
          title: 'EDA',
          description: 'Find out more about the dataset through Exploratory Data Analysis.',
          route: '/eda',
        },
        {
          title: 'Clusters',
          description: 'Explore clustering algorithms.',
          route: '/clusters',
        },
        {
          title: 'Classification',
          description: 'Understand classification methods.',
          route: '/classification',
        },
        {
          title: 'About',
          description: 'Learn more about this project.',
          route: '/about',
        },
      ],
    };
  },
};
</script>