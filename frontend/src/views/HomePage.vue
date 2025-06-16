<!-- src/views/HomePage.vue -->
<template>
  <div class="container mx-auto px-4 py-8">
    <div class="items-center flex flex-col text-center pt-[50px] lg:pt-[50px] mb-20">
      <h1 class="text-4xl sm:text-5xl sm:leading-none lg:text-7xl">
        <span class="block"> Explore the data </span>
        <span class="block text-primary font-medium"> Smell like the trend </span>
      </h1>
      <p class="max-w-md pt-2 my-3 text-sm sm:mt-5 lg:mb-0 sm:text-base lg:text-lg">
        Now that's a bold statement. Literally.
      </p>
    </div>

    <div class="flex flex-wrap justify-center -mx-2">
      <PageCard
        v-for="(card, index) in cards"
        :key="index"
        :title="card.title"
        :description="card.description"
        :route="card.route"
      />
    </div>

    <!-- ADDED TEXT SECTIONS START HERE -->
    <div class="mt-16 max-w-3xl mx-auto text-gray-700">
      <div class="mb-12 p-6 border border-gray-300 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-primary">What is this?</h2>
        <ul class="list-disc list-inside space-y-3">
          <li>
            A personal project that was originally intended for internal use only. I decided to make it public in case others might find it useful. The repository is also public, you can click the GitHub link in the top-right corner to view it.
          </li>
          <li>
            This project is essentially a glorified Jupyter Notebook - it's not meant to showcase my (questionable) frontend skills. All of the magic happens on the backend... as usual :).
          </li>
          <li>
            It’s meant to provide anyone interested in perfumes and data with some (hopefully valuable?) insight into the current perfumery landscape. Here are some questions you might ask:
            <ul class="list-disc list-inside ml-6 mt-2 space-y-1">
              <li>What makes a perfume popular - is it the scent, the longevity, the price, or all of them?</li>
              <li>Why are certain perfumes only linked to certain occasions?</li>
              <li>etc.</li>
            </ul>
            <hr>
            If you are interested in the aforementioned points, perhaps this website is worth your time.
          </li>
        </ul>
      </div>

      <div class="p-6 border border-gray-300 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-primary">What this is NOT:</h2>
        <ul class="list-disc list-inside space-y-3">
          <li>
            It’s not meant to provide any business strategy advantage or leverage. While the results and statistics may be informative, they are not conclusive due to the small sample size.
          </li>
        </ul>
      </div>

      <div class="mt-12 p-6 border border-gray-300 rounded-lg shadow-md bg-[#FFF4EA]">
        <h2 class="text-2xl font-semibold mb-4 text-primary">Data Pipeline</h2>
        <ul class="list-disc list-inside space-y-3">
          <li>
            Below is a high-level representation of the main ETL loop:
            <img
              :src="flowchart"
              alt="ETL Pipeline Diagram"
              class="w-full max-w-2xl mx-auto rounded-md shadow mt-4"
            />
          </li>
          <li>
            All data collection is performed at a non-invasive and consistently repeating time interval. If you come back to this website in about a week, chances are you will see different results!
          </li>
          <li>
            This data is also used to fine-tune a cross-encoder, which you can explore on the
            <a href="/finder" class="text-primary hover:underline">Perfume Finder</a> page.
          </li>
        </ul>
      </div>

    </div>


  </div>
</template>

<script>
import PageCard from '../components/PageCard.vue';
import apiClient from "@/api";

import flowchart from '@/assets/Flowchart_perfumedia.jpeg'

export default {
  name: 'HomePage',
  mounted() {
    this.getLatestProducts();
  },
  methods: {
    getLatestProducts() {
      apiClient.get('/test/latest-products/')
          .then(response => {
            this.latestProducts = response.data;
          }).catch(error => {
            console.log(`ERROR: BASE URL IS: ${apiClient.defaults.baseURL}\n`);
            console.log(error);
      });
    }
  },
  components: {
    PageCard,
  },
  data() {
    return {
      flowchart,
      latestProducts: [],
      cards: [
        // {
        //   title: 'ETL',
        //   description: 'See how data is Extracted, Transformed and Loaded',
        //   route: '/etl',
        // },
        {
          title: 'EDA',
          description: 'Find out more about the dataset through Exploratory Data Analysis.',
          route: '/eda',
        },
        {
          title: 'Clusters',
          description: 'Explore how the currently collected data can be clustered and described analytically',
          route: '/clusters',
        },
        {
          title: 'Perfume Finder',
          description: 'Use the information on the platform to find your dream perfume.',
          route: '/finder',
        }
       ]
    };
  },
};
</script>

<style scoped>
/* If you have a global primary color defined, you can use it.
   Otherwise, replace 'text-primary' with a specific color like 'text-indigo-600' or similar.
   For example, if your primary color is #C96868 from the previous component: */
.text-primary {
  color: #C96868; /* Example primary color */
}
</style>