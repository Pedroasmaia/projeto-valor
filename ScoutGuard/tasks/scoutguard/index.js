const fs = require('fs');
const path = require('path');
const { spawnSync, execSync } = require('child_process');
const tl = require('azure-pipelines-task-lib/task');

function resolveOutputPath(outputPath) {
  if (path.isAbsolute(outputPath)) {
    return outputPath;
  }
  const defaultWorkingDirectory = tl.getVariable('System.DefaultWorkingDirectory');
  const baseDir = defaultWorkingDirectory || process.cwd();
  return path.resolve(baseDir, outputPath);
}

function runCommand(command, args, options = {}) {
  const result = spawnSync(command, args, { encoding: 'utf8', ...options });
  if (result.error) {
    throw result.error;
  }
  if (result.status !== 0) {
    const stderr = result.stderr || '';
    const stdout = result.stdout || '';
    throw new Error(`Falha ao executar ${command} ${args.join(' ')}\n${stdout}\n${stderr}`);
  }
  return result.stdout;
}

function scoutAvailable() {
  const result = spawnSync('docker', ['scout', 'version'], { encoding: 'utf8' });
  return result.status === 0;
}

function installScout() {
  const installUrl = process.env.DOCKER_SCOUT_INSTALL_URL || 'https://raw.githubusercontent.com/docker/scout-cli/main/install.sh';
  tl.debug(`Instalando Docker Scout usando ${installUrl}`);
  execSync(`curl -sSfL ${installUrl} | sh -s --`, { stdio: 'inherit' });
}

function parseAdditionalArgs(rawArgs) {
  if (!rawArgs) {
    return [];
  }
  return rawArgs
    .split(' ')
    .map((arg) => arg.trim())
    .filter((arg) => arg.length > 0);
}

async function run() {
  try {
    const imageName = tl.getInput('imageName', true);
    const outputPath = tl.getInput('outputPath', true);
    const installScoutInput = tl.getBoolInput('installScout', true);
    const additionalArgsInput = tl.getInput('additionalArgs', false) || '';

    if (!scoutAvailable()) {
      if (!installScoutInput) {
        throw new Error('Docker Scout não está disponível e a instalação automática foi desabilitada.');
      }
      installScout();
      if (!scoutAvailable()) {
        throw new Error('Docker Scout não ficou disponível após a instalação.');
      }
    }

    const outputFile = resolveOutputPath(outputPath);
    const additionalArgs = parseAdditionalArgs(additionalArgsInput);
    const args = ['scout', 'cves', '--format', 'json', ...additionalArgs, imageName];

    tl.debug(`Executando: docker ${args.join(' ')}`);
    const output = runCommand('docker', args);

    fs.mkdirSync(path.dirname(outputFile), { recursive: true });
    fs.writeFileSync(outputFile, output, 'utf8');

    tl.setVariable('ScoutGuardReportPath', outputFile);
    tl.setResult(tl.TaskResult.Succeeded, `Relatório salvo em ${outputFile}`);
  } catch (error) {
    tl.setResult(tl.TaskResult.Failed, error.message);
  }
}

run();
