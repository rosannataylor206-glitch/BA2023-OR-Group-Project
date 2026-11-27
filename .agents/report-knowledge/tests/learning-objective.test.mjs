import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { test } from 'node:test';

test('loss choice changes the optimal constant baseline', () => {
  const labels = [0, 0, 2, 10];
  const meanLoss = (prediction, power) => labels.reduce(
    (total, label) => total + Math.abs(label - prediction) ** power, 0
  ) / labels.length;
  assert.equal(meanLoss(3, 2), 17);
  assert.equal(meanLoss(1, 1), 3);
  assert.equal(meanLoss(3, 1), 3.5);
  for (let candidate = -2; candidate <= 12; candidate += 0.25) {
    assert.ok(meanLoss(candidate, 2) >= meanLoss(3, 2));
    assert.ok(meanLoss(candidate, 1) >= meanLoss(1, 1));
    assert.ok(Math.max(...labels.map(label => Math.abs(label - candidate))) >= 5);
  }
  for (const median of [0, 0.5, 1, 1.5, 2]) assert.equal(meanLoss(median, 1), 3);
});

test('sum and mean objectives require matching penalty scales', () => {
  const labels = [2, 4];
  const sumPenalty = 2;
  const meanPenalty = sumPenalty / labels.length;
  const sumObjective = weight => labels.reduce(
    (total, label) => total + (label - weight) ** 2, 0
  ) + sumPenalty * weight ** 2;
  const meanObjective = weight => labels.reduce(
    (total, label) => total + (label - weight) ** 2, 0
  ) / labels.length + meanPenalty * weight ** 2;
  for (const weight of [-1, 0, 1, 1.5, 2, 3]) {
    assert.equal(sumObjective(weight) / labels.length, meanObjective(weight));
    assert.ok(sumObjective(weight) >= sumObjective(1.5));
  }
  assert.equal(6 / (2 + sumPenalty), 1.5);
  assert.equal(3 / (1 + sumPenalty), 1);
});

test('disjoint temporal folds can still leak future observations', () => {
  const train = [0, 1, 4, 5];
  const validation = [2, 3];
  const precedesValidation = indices => Math.max(...indices) < Math.min(...validation);
  assert.ok(train.every(index => !validation.includes(index)));
  assert.equal(precedesValidation(train), false);
  assert.equal(precedesValidation([0, 1]), true);
});

test('machine learning skill resolves its textbook card and Ridge reference', () => {
  const skill = new URL('../.agents/skills/apmcm-machine-learning/SKILL.md', import.meta.url);
  const target = '../../../research/textbook_cards/LEARNING_OBJECTIVE_AND_VALIDATION.md';
  assert.ok(readFileSync(skill, 'utf8').includes(`](${target})`));
  const card = new URL(target, skill);
  assert.ok(existsSync(card));
  assert.ok(existsSync(new URL('RIDGE_REGRESSION.md', card)));
  const text = readFileSync(card, 'utf8');
  for (const section of ['7.2.2', '7.4.2', '7.4.3']) assert.ok(text.includes(section));
});