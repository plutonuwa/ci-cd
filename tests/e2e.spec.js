import { test, expect } from '@playwright/test';

test('home page loads', async ({ page }) => {
  await page.goto('http://localhost:3000');
  const body = await page.textContent('body');
  expect(body).toContain('Hello World');
});