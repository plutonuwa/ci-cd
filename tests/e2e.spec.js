import { test, expect } from '@playwright/test';

// test('home page loads', async ({ page }) => {
//   await page.goto('http://localhost:3000');
//   const body = await page.textContent('body');
//   expect(body).toContain('Hello World');
// });

test('home page loads', async ({ page }) => {
  // Intercept network responses
  page.on('response', response => {
    if (response.url().includes('localhost:3000')) {
      response.json().then(data => {
        console.log('API Response:', JSON.stringify(data, null, 2));
      });
    }
  });

  await page.goto('http://localhost:3000');
  const body = await page.textContent('body');
  console.log('Page body:', body);
  expect(body).toContain('Hello World');
});