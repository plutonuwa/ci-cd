const request = require('supertest');
const app = require('../src/app');

describe('Routes', () => {
  test('GET / returns Hello World', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toBe(200);
    expect(res.body.message).toBe('Hello World');
  });

  test('GET /health returns ok', async () => {
    const res = await request(app).get('/health');
    expect(res.body.status).toBe('ok');
  });
});