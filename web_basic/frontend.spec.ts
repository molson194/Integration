import { test, expect, Page } from '@playwright/test';
import yaml from 'js-yaml'
import fs from 'fs'
import lodash from 'lodash'

async function setupMock(page: Page, scenario: string) {
  const doc = yaml.load(fs.readFileSync(`/Users/mols/Desktop/integration/mocks/${scenario}.yaml`, 'utf8')) as [object];
  let request_index = 0;

  await page.route('**/api/**', async (route, request) => {
    const requestUrl = new URL(request.url());
    if (requestUrl.pathname != doc[request_index]['route']) {
      throw new Error;
    }
    
    if (request.method() != doc[request_index]['method']) {
      throw new Error;
    }

    if (request.method() == 'POST' && !lodash.isEqual(request.postDataJSON(), doc[request_index]['body_params'])) {
      throw new Error;
    }
    
    await route.fulfill({ 
      json: doc[request_index]["response_body"],
      status: doc[request_index]["response_code"],
    });

    request_index += 1
  });
}


test('Basic Get', async ({ page } ) => {
  setupMock(page, 'basic_get');

  await page.goto('/');
  await expect(page.getByText('Integration')).toBeVisible();

  await page.getByText('Basic Get').click();
  await expect(page.getByText('{"basic":"get"}')).toBeVisible();
});

test('Basic Post', async ({ page }) => {
  setupMock(page, 'basic_post');

  await page.goto('/');
  await expect(page.getByText('Integration')).toBeVisible();

  await page.getByText('Basic Post').click();
  await expect(page.getByText('{"basic":"post"}')).toBeVisible();
});

test('Path Param Get', async ({ page }) => {
  setupMock(page, 'path_param_get');

  await page.goto('/');
  await expect(page.getByText('Integration')).toBeVisible();

  await page.fill('#param', 'abc');

  await page.getByText('Path Param Get').click();
  await expect(page.getByText('{"get_param":"abc"}')).toBeVisible();
});

test('Body Param Post', async ({ page }) => {
  setupMock(page, 'body_param_post');

  await page.goto('/');
  await expect(page.getByText('Integration')).toBeVisible();

  await page.fill('#param', 'xyz');

  await page.getByText('Body Param Post').click();
  await expect(page.getByText('{"post_param":"xyz"}')).toBeVisible();
});

test('Two Requests', async ({ page }) => {
  setupMock(page, 'two_requests');

  await page.goto('/');
  await expect(page.getByText('Integration')).toBeVisible();

  await page.fill('#param', 'xyz');

  await page.getByText('Body Param Post').click();
  await expect(page.getByText('{"post_param":"xyz"}')).toBeVisible();

  await page.getByText('Path Param Get').click();
  await expect(page.getByText('{"get_param":"xyz"}')).toBeVisible();
});
