=======
# Professor Qiao Dandan Website
Portfolio Website for Professor Qiao DanDan.

# Developer Setup
1. Clone the repository.
2. Ensure latest Node.js is installed.
3. Run ```npm install``` to install packages.
4. ```npm run dev``` for local preview.
5. ```npm run deploy``` to push to GitHub Pages.

# How to Update Site Content
Site content is defined in ```data/siteContent.tsx```.
  
## Publications
There are 4 types of publications: journalPublications, conferencePublications, underReviewPublications, workingPaperPublications.   
The arrays for these publication objects can be found in ```data/siteContent.tsx```.
Each item has fields: 
* **year** (required): Year in numerical form. Can be an empty string. Publications will be sorted in descending order based on year.
* **text** (required): Should be wrapped in html formatting like this ```(<>text</>)```. Tags ```<b></b>``` or ```<i></i>``` can be used to format the text.
* **href** (optional): Used to add a website link. If added, the publication card on the website will be clickable and lead to the website.
  
## Students
There are 2 types of students: alumniItems, studentItems
The arrays for these student objects can be found in ```data/siteContent.tsx```.
Each item has fields:
* **name** (required): Name of the student / alumni.
* **description** (required): Description of the student / alumni. 
* **startYear** (required): Start of candidature. Students are arranged according to startYear in ascending order.
* **endYear** (optional): End of candidature (not added for non-alumni). Alumni are arranged according to endYear in descending order.
* **picture** (optional): Picture files should be added to ```public/alumni``` and ```public/students``` folders. This field should have the path (e.g. ```alumni/ying-lu.webp```).
* **pictureAlt** (optional): Alt text for picture.
* **profileUrl** (optional): Link to the student / alumni's website. If added, the student's card will be clickable and lead to the website. 


# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])

```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])

```

