import {
  JupyterFrontEnd, JupyterFrontEndPlugin
} from '@jupyterlab/application';


/**
 * Initialization data for the simple-git extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'simple-git',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension simple-git is activated!');
  }
};

export default extension;
